import os
os.chdir(os.path.join(os.getcwd(), 'patcher'))

from updater import download_latest_version
download_latest_version()




