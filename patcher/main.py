from GDrive import DriveUtil
from file_utils import unzip_file
from updater import download_latest_version
import os
gDrive = DriveUtil()
gDrive.upload_to_drive()
gDrive.share_file_to_public()

file_id = gDrive.remote_file_info["id"]
destination = './temporary.zip'
gDrive.download_file_from_google_drive(file_id, destination)

unzip_file("./temporary.zip", "./Game_Files", deleteZip=False)




while True:
    try:
        os.chdir('./patcher')
        print(os.getcwd())
        download_latest_version()
        restart = input('\nFinished; run again? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break
    except FileNotFoundError:
        print(os.getcwd())
        download_latest_version()
        restart = input('\nFinished; run again? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

#TODO: Jake Topics
#TODO: Docker

#TODO: now get all of the created functions + updating yamal + compressing files
#TODO: together to run in an appropriate main file (also have update yamal function delete intermediate version_test.txt file
#TODO: which was created by zip_file_with_VERSION
#TODO: After completing structure, update readme.md and add concept diagram of information flow

#use credentials through credentials.json

#T #detail how to get refresh token/create credentials in readme.md, read up on how to write markdown(.md)
#go to https://developers.google.com/adwords/api/docs/guides/authentication
#and https://console.developers.google.com/apis and click credentials
