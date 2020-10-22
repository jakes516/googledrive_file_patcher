# Google Drive Game Patcher

## Description
This repository is a patcher for uploading, downloading, and unzipping google drive files, opening the drive files to public access, 
and keeping file versions updated. The code uses Python 3.7 (Pycharm IDE) with re, requests, os, yaml, pathlib, json, zipfile, and OAuth2Service modules installed.
(All dependencies listed in requirements.txt)

## Getting Started
All code is contained within the [*patcher*](patcher) directory, and as of now the patcher is completely functional.


I suggest creating a virtual environment by using your command line/shell to `cd` into the *googledrive_game_patcher* directory, and running the command `python -m venv venv`. 
I have included a [*requirements.txt*](requirements.txt) file to easily install all dependencies. Navigate to the *Scripts* directory of the above/your venv, cut the included [*requirements.txt*](requirements.txt) file, 
and paste it in the *Scripts* directory. Then run the command `pip install -r requirements.txt` in your command line/shell.
Your environment setup should be ready to go.


Be sure to store your desired upload file in the [*File_of_interest*](patcher/File_of_interest) directory, 
and change the [*raw github yaml url*](patcher/version_history/versions.yaml) (stored in the variable "ver_URL") to your repository's at the top of [*updater*.**download_the_latest_version**](patcher/updater.py).

And in [*GDrive*.**delete_files_from_drive**](patcher/GDrive.py).(It is the 7th method of DriveUtil). 

Also be sure to create OAuth2 Playground Credentials detailed below in the Uploader Setup section.

## Functionality
[*Main.py*](patcher/main.py) now compresses the file you have in [*File_of_interest*](patcher/File_of_interest) with a prompt for version number, uploads the zipfile with a [*VERSION.txt*](patcher/Game_Files/VERSION.txt) to drive,
opens this file for public access/sharing, updates the local [*versions.yaml*](patcher/version_history/versions.yaml) file and pushes this update to github.

A separate [*download_file.py*](patcher/download_file.py) now downloads the latest version listed on your github's [*versions.yaml*](patcher/version_history/versions.yaml) from drive.

The [*uploader.sh*](uploader.sh) and [*downloader.sh*](downloader.sh) files have now been added and are functional; they run the *shell_file.py*'s which contain modified paths for [*Main.py*](patcher/main.py) and [*download_file.py*](patcher/download_file.py).
The command line window is left open to read, press enter to close it after they have run.

[*GDrive.py*](patcher/GDrive.py), [*file_utils.py*](patcher/file_utils.py), and [*updater.py*](patcher/updater.py) are where all important functions are coded.

## Structure
- Google Drive + Drive API v3
- OAuth2 Playground
- Github Repository
- Local Storage with Game File + versions.yaml File

<p align="center">
    <img width="811" height="480" src="Documentation/Patcher_Structure.jpg">
</p>


## Uploader Setup
In order to run the uploader portion of this code you will need to create a [Google Account](https://accounts.google.com/signup/v2/webcreateaccount?hl=en&flowName=GlifWebSignIn&flowEntry=SignUp) and access your [Google Drive](https://drive.google.com/). 
You will also need to authorize credentials for a web application in the Google developers console and obtain a permanent refresh token from OAuth2Playground. 
Follow the link below to generate your account OAuth2 Playground credentials.

- Skip down to section named **OAuth2 Playground** [Create OAuth2 Credentials](https://developers.google.com/adwords/api/docs/guides/authentication)

##### **IMPORTANT**
Be sure to rename the provided [*Credentials_placeholder*](patcher/Credentials_placeholder) directory to "Credentials" and the rename the existing [*client_credentials_placeholder.json*](patcher/Credentials_placeholder/client_credentials_placeholder.json) file to "client_credentials.json".
The patcher functions depend on these specific credential file names for relative paths.

Once you have generated the Client Secret, Client ID, and refresh token credentials open the newly-named *client_credentials.json* file and enter/paste them into the labeled placeholder spots. 
Be sure to add the *Credentials* directory to your .gitignore (save patcher/Credentials/ in .gitignore) as this info grants access to your account.





## Downloader Setup
In order for the downloader to run appropriately you need a [*VERSION.txt*](patcher/Game_Files/VERSION.txt) file with the current file version number listed in it present in your [*Game_files*](patcher/Game_Files) directory.
If you do not have a [*VERSION.txt*](patcher/Game_Files/VERSION.txt) it will automatically clear your [*Game_files*](patcher/Game_Files) directory and download the latest game files from Google Drive.

## Future Updates
Will update this readme if there are any future developments.
