import json
import os
import requests
from rauth import OAuth2Service

#bearer token generator for google drive api
class ExampleOAuth2Client:
    def __init__(self, client_id, client_secret):
        self.access_token = None

        self.service = OAuth2Service(
            name="Patcher",
            client_id=client_id,
            client_secret=client_secret,
            access_token_url="https://oauth2.googleapis.com/token",
            authorize_url="https://accounts.google.com/o/oauth2/v2/auth",
            base_url="https://www.googleapis.com",
        )

        self.get_access_token()

    def get_access_token(self):
        data = {
            #refresh token generated on Oauth2.0playground goes below
            'refresh_token': 'refresh_token_generated_using_above_here',
            'grant_type': 'refresh_token',
            'redirect_uri': 'https://developers.google.com/oauthplayground'}

        session = self.service.get_auth_session(data=data, decoder=json.loads)

        self.access_token = session.access_token
        return session.access_token


#enter the client_id, client_secret credentials created on console.developers.google.com here
Auth2Client = ExampleOAuth2Client('client_id',
                                      'client_secret')



#drive utility for downloading, uploading, sharing
class DriveUtil:
    '''
    This is a google drive util to upload files to google drive, download them, and open the file for public access

    '''
    def __init__(self):
        self.access_token = str(Auth2Client.get_access_token())
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
        #assign path to file being uploaded as filename
        filename = r'C:\Users\Jake\Pictures\v1.0.0.jpg.zip'
        filesize = os.path.getsize(filename)
        headers = {"Authorization": "Bearer " + self.access_token, "Content-Type": "application/json"}
        params = {
            "name": "v1.0.0.jpg.zip",
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




