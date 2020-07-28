import json
import os
import requests


class DriveUtil:
    '''
    This is a google drive util to upload files to google drive, download them, and open the file for public access

    '''
    def __init__(self):
        self.access_token = 'ya29.a0AfH6SMBGr2RdIJeP-0ZORbYt4Aezi0pMukqsF_jdiY9XIicjccTvlQAbOh4EZpESE4ypQSDs6whGgBz9TmFCQFeCDi5_9wScMBOxCx2BOXcWeHACQelx0TQ6GxxT_aPU9avxiRt9lUVRh0vDdNL0zALt0n3xV1YKXW0'
    #alert deleting everything in temp before download (google how to delete stuff from temp (maybe shutil)
    def download_file_from_google_drive(self, file_id, destination):
        URL = "https://docs.google.com/uc?export=download"

        session = requests.Session()

        response = session.get(URL, params={'id': file_id}, stream=True)
        token = self.get_confirm_token(response)

        if token:
            params = {'id': file_id, 'confirm': token}
            response = session.get(URL, params=params, stream=True)

        self.save_response_content(response, destination)


    def get_confirm_token(self, response):
        for key, value in response.cookies.items():
            if key.startswith('download_warning'):
                return value

        return None

    def save_response_content(self, response, destination):
        CHUNK_SIZE = 32768

        with open(destination, "wb") as f:
            for chunk in response.iter_content(CHUNK_SIZE):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)

    def upload_to_drive(self):
        filename = r'C:\Users\Jake\Pictures\walter c dornez.zip'
        filesize = os.path.getsize(filename)
        headers = {"Authorization": "Bearer " + self.access_token, "Content-Type": "application/json"}
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

        headers = {"Content-Range": "bytes 0-" + str(filesize - 1) + "/" + str(filesize)}
        r = requests.put(
            location,
            headers=headers,
            data=open(filename, 'rb')
        )
        print(r.text)
        self.remote_file_info = json.loads(r.text)

    def share_file_to_public(self):
        id = self.remote_file_info["id"]
        url = f"https://www.googleapis.com/drive/v3/files/{id}/permissions"

        payload = "{\"role\": \"reader\", \"type\": \"anyone\"}"
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        print(response.text.encode('utf8'))


    #TODO: Need to delete files
    def delete_file_from_drive(self):
        pass

    #TODO: Need to generate bearer token
    def generate_access_token_through_oauth2(self):
        # Allegedly. Untested.
        # https://stackoverflow.com/questions/36719540/how-can-i-get-an-oauth2-access-token-using-python
        pass





