import os

#Changing cwd to work with .sh file.
os.chdir(os.path.join(os.getcwd(), 'patcher'))

from updater import download_latest_version
download_latest_version()




