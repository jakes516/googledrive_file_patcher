import os

os.chdir(os.path.join(os.getcwd(), 'patcher'))

from GDrive import DriveUtil

if __name__ == '__main__':
    #Name your zip file to be uploaded to drive
    zip_name = str('your_game_zipfile.zip')
    gDrive = DriveUtil()
    gDrive.zip_file_with_VERSION(zip_name)

    gDrive.upload_to_drive(zip_name)

    gDrive.share_file_to_public()

    gDrive.update_yaml()

    gDrive.auto_git_update_yaml()
