#read a file to check the current version
#go to github for versions.yaml, check latest version there and compare with current
#if they are not =, update with current one in versions.yaml, use gdrive.download_file_from_drive with file_id from versions.yaml
#download all to temp, replace version in current directory
#refactor code


from file_utils import unzip_file
from GDrive import DriveUtil
import yaml
import requests
import pathlib

def update_version():
    for path in pathlib.Path("./temp").iterdir():
        if path.is_file():
            current_file = open(path, "r")
    ver_URL = "https://raw.githubusercontent.com/jakes516/tempgame_patcher/master/versions.yaml"
    session = requests.Session()
    response = session.get(ver_URL)
    versions = yaml.load(response.text, Loader = yaml.FullLoader)

    #print(versions)

    latest_version = versions['version'][0]
    latest_version_id = versions['version'][0]['v1.0.0']['file_id']

    #print(latest_version_id)

    for version_number, id in latest_version.items():
        latest_version_number = version_number

    #print(latest_version_number)
    #print(current_file.name)
    file_id = latest_version_id
    if latest_version_number in current_file.name:
        print(f"Your version ({latest_version_number}) is up to date")
        return
    else:
        print(f"Your version is not up to date. {latest_version_number} update is downloading.")
        current_file.close()
        gDrive = DriveUtil()
        destination = './temporary.zip'
        gDrive.download_file_from_google_drive(file_id, destination)
        unzip_file("./temporary.zip", "./temp", deleteZip=False)

