
from file_utils import unzip_file
from GDrive import DriveUtil
import yaml
import requests

#Checks current file version and downloads latest if not up to date.
def download_latest_version():
    #Getting versions.yaml info from github. Enter the raw github url to your versions.yaml as ver_URL below.
    ver_URL = "https://raw.githubusercontent.com/jakes516/googledrive_game_patcher/master/patcher/version_history/versions.yaml"
    session = requests.Session()
    response = session.get(ver_URL)
    versions = yaml.load(response.text, Loader = yaml.FullLoader)
    print(versions)

    latest_version = versions['version'][0]

    #Getting version file_id for drive download.
    for version_number, id in latest_version.items():
        latest_version_number = version_number
        file_id = id['file_id']

    #Running loop to check if you have version.txt and compare your version number to the github one.
    while True:
        try:
            current_file = open('./Game_Files/VERSION.txt')
        except FileNotFoundError:
            print('Uh oh you do not have a VERSION.txt in your Game_Files directory . . . let me download the latest folder with it.')
            gDrive = DriveUtil()
            destination = './temporary.zip'
            gDrive.download_file_from_google_drive(file_id, destination)
            unzip_file("./temporary.zip", "./Game_Files", deleteZip=False)
            break
        if latest_version_number == current_file.read():
            print(f"Your version ({latest_version_number}) is up to date")
            current_file.close()
            break
        else:
            print(f"Your version is not up to date. {latest_version_number} update is downloading.")
            current_file.close()
            gDrive = DriveUtil()
            destination = './temporary.zip'
            gDrive.download_file_from_google_drive(file_id, destination)
            unzip_file("./temporary.zip", "./Game_Files", deleteZip=False)
            break
