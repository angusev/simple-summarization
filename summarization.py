from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from typing import List
from langchain.chains import MapReduceDocumentsChain, ReduceDocumentsChain
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import ChatOpenAI
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.chains.llm import LLMChain
from langchain.prompts import PromptTemplate
from langchain.docstore.document import Document
from dotenv import load_dotenv
import asyncio
from typing import List


app = FastAPI()

load_dotenv()
llm = ChatOpenAI(temperature=0, model="gpt-4-turbo-preview")

map_template = """The following is a set of documents
{docs}
Based on this list of docs, please prepare a brief summary
Helpful Answer:"""

reduce_template = """The following is set of summaries:
{docs}
Take these and distill it into a final, consolidated summary of the document. 
Helpful Answer:"""

map_prompt = PromptTemplate.from_template(map_template)
reduce_prompt = PromptTemplate.from_template(reduce_template)

map_chain = LLMChain(llm=llm, prompt=map_prompt)
reduce_chain = LLMChain(llm=llm, prompt=reduce_prompt)

combine_documents_chain = StuffDocumentsChain(
    llm_chain=reduce_chain, document_variable_name="docs"
)

reduce_documents_chain = ReduceDocumentsChain(
    combine_documents_chain=combine_documents_chain,
    collapse_documents_chain=combine_documents_chain,
    token_max=4000,
)

map_reduce_chain = MapReduceDocumentsChain(
    llm_chain=map_chain,
    reduce_documents_chain=reduce_documents_chain,
    document_variable_name="docs",
    return_intermediate_steps=False,
)

text_splitter = CharacterTextSplitter.from_tiktoken_encoder(
    chunk_size=1000, chunk_overlap=0
)

def run(text_to_process: str):
    split_docs = text_splitter.split_text(text_to_process)

    documents = [Document(page_content=doc) for doc in split_docs]

    return map_reduce_chain.run(documents)