import json
import os
import requests
from rauth import OAuth2Service
import yaml
import re
import zipfile

# Bearer token generator for google drive api
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
        # Loading json file with client_id, client_secret, refresh_token

        cred = open(str(os.path.join(os.getcwd(), 'Credentials\client_credentials.json')))
        credentials = json.load(cred)
        cred.close()
        data = {
            # Refresh token generated on Oauth2.0playground is placed below from your credentials.json

            'refresh_token': str(credentials['refresh_token']),
            'grant_type': 'refresh_token',
            'redirect_uri': 'https://developers.google.com/oauthplayground'}

        session = self.service.get_auth_session(data=data, decoder=json.loads)

        self.access_token = session.access_token
        return session.access_token


# Loading credentials info to be used for auth.
cred = open(str(os.path.join(os.getcwd(), 'Credentials\client_credentials.json')))
credentials = json.load(cred)
cred.close()

# The client_id, client_secret credentials created on console.developers.google.com placed here using your credentials.json.

# Authorizing using credentials.
Auth2Client = ExampleOAuth2Client(str(credentials['client_id']),
                                      str(credentials['client_secret']))



# Drive utility for downloading, zipping/version, uploading, sharing, and updating versions.yaml.
class DriveUtil:
    '''
    This is a google drive util to upload files to google drive, download them, and open the file for public access

    '''
    def __init__(self):
        #Defining access token you generated for all upload code being run.

        self.access_token = str(Auth2Client.get_access_token())


    def download_file_from_google_drive(self, file_id, destination):
        # Drive download function used in updater.py

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

    def upload_to_drive(self, zip_name):
        # Naming file and uploading to drive

        filename = f'./{zip_name}'
        filesize = os.path.getsize(filename)
        headers = {"Authorization": "Bearer " + self.access_token, "Content-Type": "application/json"}
        params = {
            "name": f"{self.version_input}.zip",
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
        # Enabling public access to drive file through file_id link.

        id = self.remote_file_info["id"]
        url = f"https://www.googleapis.com/drive/v3/files/{id}/permissions"

        payload = "{\"role\": \"reader\", \"type\": \"anyone\"}"
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        print(response.text.encode('utf8'))




    # Deletes all old versions listed in yaml from drive
    def delete_files_from_drive(self):
        ver_URL = "https://raw.githubusercontent.com/jakes516/tempgame_patcher/master/versions.yaml"
        session = requests.Session()
        response = session.get(ver_URL)
        versions = yaml.load(response.text, Loader=yaml.FullLoader)

        version_history = versions['version_history']
        file_ids_comp = []

        for numbers in range(len(version_history)):
            file_ids_comp.append(list(version_history[numbers].values()))


        file_ids = []

        for ids in range(len([file_ids_comp]) + 1):
            file_ids.append(file_ids_comp[ids][0]['file_id'])

        headers = {"Authorization": "Bearer " + self.access_token, "Content-Type": "application/json"}

        for id_value in file_ids:
            r = requests.delete(f"https://www.googleapis.com/drive/v3/files/{id_value}",
                                headers=headers)

    # Function to automate updating local yamal, developing automated add, commit, push to github
    # Must be run IMMEDIATELY following the upload function
    def update_yaml(self):
        id = self.remote_file_info["id"]

        file_id_numbers = id
        file_name = "./version_history/versions.yaml"
        try:
            version_txt_file = "./VERSION_temporary.txt"
        except FileNotFoundError:
            print('You have not zipped and uploaded a new file and version_file since your last yaml update.')
        try:
            with open(file_name) as local_yaml:
                # Finding latest version from yaml.
                version_info = yaml.safe_load(local_yaml)
                print(version_info)
                latest_version = version_info['version'][0]

                # Finding latest version number.
                for version_number, id in latest_version.items():
                    latest_version_number = version_number
                print(latest_version_number)

                #Comparing latest version number with current local version, and updating if different.
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
        except FileNotFoundError:
            # Creates yaml file placeholder to be updated if you do not have one
            print("You do not have a versions.yaml file . . . let me make one for you.")
            yaml_version_format = {'version': [{'version.placeholder': {'file_id.placeholder': 'id.placeholder'}}],
                                   'version_history': [{'v.placeholder': {'file_id.placeholder': 'id.placeholder'}}]}
            yaml_string_format = str(yaml.dump(yaml_version_format))

            save_path = str(os.path.join(os.getcwd(), 'version_history'))
            completeName = os.path.join(save_path, 'versions.yaml')
            with open(completeName, "w") as f:
               f.write(yaml_string_format)
        os.remove('./VERSION_temporary.txt')


    def auto_git_update_yaml(self):
        # Automatically adds, commits, and pushes to github.

        os.chdir('..')
        os.system('git add patcher/version_history')
        os.system('git commit -m "auto version_history.yaml update')
        os.system('git push origin master')

    def zip_file_with_VERSION(self, zip_name):
        # Zips file, and prompts version number user input.

        for filename in os.listdir("File_of_interest"):
            file = str(os.path.join(os.getcwd(), "File_of_interest\\"+filename))
        game_name = file.rsplit('\\', 1)

        while True:

            self.version_input = str(input("\nPlease type the version number in the form v##.##.##\n"))
            regex = re.compile(r"^[vV](\d\d.){2}\d\d$")
            if regex.match(self.version_input):
                with open('VERSION_temporary.txt', 'w') as f:
                    f.write(self.version_input)
                print("Version number updated.")
                break
            else:
                print("\nThe version number you entered is in an improper form. \nPlease re-enter the version number\n")
                continue

        # Zips chosen file with version.txt file.
        with zipfile.ZipFile(zip_name, 'w') as myzip:

            myzip.write(file, arcname=game_name[1])
            myzip.write('./VERSION_temporary.txt', arcname = './VERSION.txt')


