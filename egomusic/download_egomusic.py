from egomusic.utils import *

# Download EgoMusic from Zenodo
url = 'https://zenodo.org/records/16753794/files/EgoMusic.zip'
filename = 'EgoMusic.zip'
download_file(url, filename)

# Unzip downloaded file and remove the zip file.
target_directory = './data/'
unzip_file(filename, target_directory)
