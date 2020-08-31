import json
import os
import requests
from rauth import OAuth2Service
import yaml
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
        #loading json file with client_id, client_secret, refresh_token
        cred = open('./Credentials/client_credentials.json')
        credentials = json.load(cred)
        cred.close()
        data = {
            #refresh token generated on Oauth2.0playground goes below
            'refresh_token': str(credentials['refresh_token']),
            'grant_type': 'refresh_token',
            'redirect_uri': 'https://developers.google.com/oauthplayground'}

        session = self.service.get_auth_session(data=data, decoder=json.loads)

        self.access_token = session.access_token
        return session.access_token



cred = open('./Credentials/client_credentials.json')
credentials = json.load(cred)
cred.close()

#enter the client_id, client_secret credentials created on console.developers.google.com here
Auth2Client = ExampleOAuth2Client(str(credentials['client_id']),
                                      str(credentials['client_secret']))



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

        ## ./patcher/test_file.zip change path to relative path in directory
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


# immediately Update yaml file on github following an upload by pulling yaml and comparing current version to version.txt of upload

# re-organize upload/download directories and create function to zip game file and prompt version in VERSION.txt prior to upload,

    #deletes all old versions listed in yaml from drive
    def delete_files_from_drive(self):
        ver_URL = "https://raw.githubusercontent.com/jakes516/tempgame_patcher/master/versions.yaml"
        session = requests.Session()
        response = session.get(ver_URL)
        versions = yaml.load(response.text, Loader=yaml.FullLoader)
        # print(versions)
        version_history = versions['version_history']
        file_ids_comp = []
        # print(version_history)

        for numbers in range(len(version_history)):
            file_ids_comp.append(list(version_history[numbers].values()))
        #print(file_ids_comp)

        file_ids = []

        for ids in range(len([file_ids_comp]) + 1):
            file_ids.append(file_ids_comp[ids][0]['file_id'])
        #print(file_ids)

        headers = {"Authorization": "Bearer " + self.access_token, "Content-Type": "application/json"}

        for id_value in file_ids:
            r = requests.delete(f"https://www.googleapis.com/drive/v3/files/{id_value}",
                                headers=headers)

# develop function to automate updating local yamal, then push to github
    #must be run IMMEDIATELY following the upload function
    def update_yaml(self):
        id = self.remote_file_info["id"]
        # why was naming it twice necessary for obtaining the file_id, using only id only gave the dictionary
        file_id_numbers = id
        file_name = "./version_history/versions.yaml"
        try:
            version_txt_file = "./VERSION_test.txt"
        except FileNotFoundError:
            print('You have not zipped and uploaded a new file and version_file since your last yaml update.')
        with open(file_name) as local_yaml:
            version_info = yaml.safe_load(local_yaml)
            print(version_info)
            latest_version = version_info['version'][0]
            for version_number, id in latest_version.items():
                latest_version_number = version_number
            print(latest_version_number)
            with open(version_txt_file) as version_txt_file_open:
                new_version = version_txt_file_open.read()
                if latest_version_number in version_txt_file_open:
                    print("It appears your yaml already contains this latest version info.")
                else:
                    outdated_version = version_info['version'][0]
                    version_info['version_history'].insert(0,outdated_version)
                    version_info['version'][0] = {f'{new_version}': {'file_id': f'{file_id_numbers}'}}
                    with open(file_name, 'w+') as local_yaml:
                        yaml.safe_dump(version_info, local_yaml)
                    #print(id)
#TODO make update yamal function delete existing version_test.txt


