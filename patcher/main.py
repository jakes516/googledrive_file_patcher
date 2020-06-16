from GDrive import DriveUtil
from file_utils import unzip_file


gDrive = DriveUtil()
gDrive.upload_to_drive()
gDrive.share_file_to_public()

file_id = gDrive.remote_file_info["id"]
destination = './temporary.zip'
gDrive.download_file_from_google_drive(file_id, destination)

unzip_file("./temporary.zip", "./temp", deleteZip=False)

#TODO: Jake Topics
#TODO: Docker