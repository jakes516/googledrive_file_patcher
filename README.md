# Google Drive Game Patcher

## Description
This repository is a patcher for uploading, downloading, and unzipping google drive files, opening the drive files to public access, 
and keeping file versions updated. The code uses Python 3.7 (Pycharm IDE) with re, requests, os, yaml, pathlib, json, zipfile, and OAuth2Service modules installed.

As of now the patcher is completely functional, be sure you create Credentials detailed below in Uploader Setup, store your desired upload file in the File_of_interest directory, 
and the github yaml url is changed to yours in updater and GDrive's delete_files_from_drive. 

Main.py now compresses the file you have in File_of_interest with a prompt for version number, uploads the zipfile with a version.txt to drive,
opens this file for public access/sharing, updates the local version_history.yaml file and pushes this update to github.

A separate download_latest_file.py now downloads the latest version listed on your github's version_history.yaml from drive.

The uploader.sh and downloader.sh files have now been added and are fucntional; they run the shell_file.py's which contain modified paths for main.py and download_latest_file.py.

## Structure
- Google Drive + Drive API v3
- OAuth2 Playground
- Github Repository
- Local Storage with Game File + versions.yaml File

<p align="center">
    <img width="811" height="480" src="Documentation/Patcher_Structure.jpg">
</p>


## Uploader Setup
In order to run the uploader portion of this code you will need to create a google account and access your google drive. 
You will also need to authorize credentials for a web application in the Google developers console and obtain a permanent refresh token from OAuth2Playground. 
Follow the links below to generate your account credentials.
 
- [Create Google Account](https://accounts.google.com/signup/v2/webcreateaccount?hl=en&flowName=GlifWebSignIn&flowEntry=SignUp)
- [Google Drive](https://drive.google.com/)
- Create Authorization Credentials [OAuth2 Authenication](https://developers.google.com/adwords/api/docs/guides/authentication)
- [Google Developers Console](https://console.developers.google.com/)

Once you have generated the Client Secret, Client ID, and refresh token credentials you should save them in a "Credentials" subdirectory as a .json file in the patcher directory. 
Be sure to add the credentials.json file to your .gitignore as this info grants access to your account.





## Downloader Setup
In order for the downloader to run appropriately you need a VERSION.txt file with the current file version number listed in it present in your Game_Files directory.
If you do not have a VERSION.txt it will automatically clear your Game_files directory and download the latest game files from Google Drive.

## Future Updates
Will update this read_me if there are any future developments.
