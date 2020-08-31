import zipfile
import os
import re

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


#TODO automate zipping and prompting version number

#An intermediate VERSION.txt file will be created during this process outside of the zip file within the patcher directory.
# DO NOT DELETE THIS, it is necessary for updating the yaml, the update yaml function will delete it after it finishes.
def zip_file_with_VERSION(zip_name, file):
    while True:

            version_input = str(input("\nPlease type the version number in the form v#.#.#\n"))
            regex = re.compile(r"^[vV](\d.){2}\d$")
            if regex.match(version_input):
                with open('VERSION_test.txt', 'w') as f:
                    f.write(version_input)
                print("Version number updated.")
                break
            else:
                print("\nThe version number you entered is in an improper form. \nPlease re-enter the version number\n")
                continue

    with zipfile.ZipFile(zip_name, 'w') as myzip:

        #enter arcname = to relative game file name
        myzip.write(file, arcname='./wasp.jpg')
        myzip.write('./VERSION_test.txt')
        #os.remove('./VERSION_test.txt')
        #enter path to game projects directory
#zip_file_with_VERSION('test_file.zip', "C:/Users/Jake/Pictures/wasp.jpg")
