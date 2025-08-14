import requests
import sys
import zipfile
import os

# Function to download a file from a URL
def download_file(url, filename):

    print(f'Downloading file from: {url}.')
    print(f'Saving to: {filename}')
    
    response = requests.get(url, stream=True)
    response.raise_for_status()

    total_size = int(response.headers.get('content-length', 0))

    downloaded_size = 0
    chunk_size = 8192

    with open(filename, 'wb') as f:
        for chunk in response.iter_content(chunk_size=chunk_size):
            if chunk:
                f.write(chunk)
                downloaded_size += len(chunk)

                if total_size > 0:
                    progress = (downloaded_size / total_size) * 100
                    print(f'Downloaded: {downloaded_size / (1024*1024):.2f}MB / {total_size / (1024*1024):.2f}MB ({progress:.2f}%)', end='\r')
                else:
                    print(f'Downloaded: {downloaded_size / (1024*1024):.2f}MB', end='\r')
                sys.stdout.flush()
    
    print('\nDownload complete.')

# Download EgoMusic from Zenodo
url = 'https://zenodo.org/records/16753794/files/EgoMusic.zip'
filename = 'EgoMusic.zip'
download_file(url, filename)

# Unzip downloaded file and remove the zip file.
target_directory = './egomusic/'
with zipfile.ZipFile(filename, 'r') as zip_ref:
    zip_ref.extractall(target_directory)
    print(f'{filename} files extracted.')
os.remove(filename)
