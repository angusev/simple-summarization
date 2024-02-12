import requests


def test_upload(endpoint_url, file_path):
    files = {"file": (file_path, open(file_path, "rb"), "text/plain")}
    response = requests.post(endpoint_url, files=files)

    if response.status_code == 200:
        print("Upload successful.")
        print("Response:", response.json())
    else:
        print("Upload failed.")
        print("Status Code:", response.status_code)
        print("Response:", response.text)


if __name__ == "__main__":
    UPLOAD_ENDPOINT = "https://simple-summarization.onrender.com/upload/"

    FILE_PATH = "./testing/test.txt"

    test_upload(UPLOAD_ENDPOINT, FILE_PATH)
