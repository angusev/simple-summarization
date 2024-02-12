map_template = """The following is a set of documents
{docs}
Based on this list of docs, please prepare a brief summary
Helpful Answer:"""

reduce_template = """The following is set of summaries:
{docs}
Take these and distill it into a final, consolidated summary of the document. 
Helpful Answer:"""

TOKEN_MAX = 4000
CHUNK_SIZE = 1000
