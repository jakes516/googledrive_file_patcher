from GDrive import DriveUtil
from file_utils import unzip_file
from updater import download_latest_version
import os




#file_id = gDrive.remote_file_info["id"]
#destination = './temporary.zip'
#gDrive.download_file_from_google_drive(file_id, destination)

#unzip_file("./temporary.zip", "./Game_Files", deleteZip=False)




# while True:
#     try:
#         os.chdir('./patcher')
#         print(os.getcwd())
#         download_latest_version()
#         restart = input('\nFinished; run again? Enter yes or no.\n')
#         if restart.lower() != 'yes':
#             break
#     except FileNotFoundError:
#         print(os.getcwd())
#         download_latest_version()
#         restart = input('\nFinished; run again? Enter yes or no.\n')
#         if restart.lower() != 'yes':
#             break
#TODO: Now finish fixing paths to relative paths, have update yaml function auto push to github,
#TODO: have zip_file_with_VERSION use version input for google drive naming in upload to drive params
#TODO:

gDrive = DriveUtil()
gDrive.zip_file_with_VERSION('test_file.zip', "./File_of_interest/wasp.jpg")

gDrive.upload_to_drive()

gDrive.share_file_to_public()

gDrive.update_yaml()












#TODO: Jake Topics
#TODO: Docker

#TODO: After completing structure, update readme.md and add concept diagram of information flow

#use credentials through credentials.json

#T #detail how to get refresh token/create credentials in readme.md, read up on how to write markdown(.md)
#go to https://developers.google.com/adwords/api/docs/guides/authentication
#and https://console.developers.google.com/apis and click credentials
