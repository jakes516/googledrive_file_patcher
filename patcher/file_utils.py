import zipfile
import os

#unzips file and removes older files in directory
def unzip_file(file, destination, deleteZip = True):
    if os.path.exists(destination):
        filelist = [f for f in os.listdir(destination)]
        for f in filelist:
            os.remove(os.path.join(destination, f))

    with zipfile.ZipFile(file, 'r') as zip_ref:
        zip_ref.extractall(destination)

    if deleteZip:
        os.remove(file)