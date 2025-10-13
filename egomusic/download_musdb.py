import os
from egomusic.utils import *

# Download MUSDB18-HQ if not available
musdb_path = './data/musdb18/'

# Create musdb folder if it does not exists.
os.makedirs(musdb_path, exist_ok=True)

# Download musdb18 if there are no files
if len(os.listdir(musdb_path)) == 0:
    print(f'MUSDB18 files are not downloaded. Downloading MUSDB18...')

    # Download MUSDB18-HQ from Zenodo
    url = 'https://zenodo.org/records/3338373/files/musdb18hq.zip?download=1'
    filename = 'musdb18hq.zip'
    download_file(url, filename)

    # Unzip downloaded file and remove the zip file.
    unzip_file(filename, musdb_path)
else:
    print(f'MUSDB18 files are already downloaded.')
