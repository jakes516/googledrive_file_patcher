import json
import os
import requests

access_token = 'ya29.a0AfH6SMAUhwxiNZ7yFNqB9zFFdbMninrzDW54srSdigaSffRxShTN_q3eDYVPLi6QrWR8_HNKf3ZgJLT2rPkZmM94K3SFQGkBWYVjtwfspo-U0f3YtdheVv0ieSK8h-EBH6JgfegLlv2yEgbqCNfwGQsBmRD7Wg_oSGs'  ## Please set the access token.

filename = r'C:\Users\Jake\Pictures\walter c dornez.zip'

filesize = os.path.getsize(filename)

# 1. Retrieve session for resumable upload.

headers = {"Authorization": "Bearer "+access_token, "Content-Type": "application/json"}
params = {
    "name": "test.zip",
    "mimeType": "application/zip"
}
r = requests.post(
    "https://www.googleapis.com/upload/drive/v3/files?uploadType=resumable",
    headers=headers,
    data=json.dumps(params)
)
location = r.headers['Location']
print(r)
# 2. Upload the file.

headers = {"Content-Range": "bytes 0-" + str(filesize - 1) + "/" + str(filesize)}
r = requests.put(
    location,
    headers=headers,
    data=open(filename, 'rb')
)
print(r.text)

