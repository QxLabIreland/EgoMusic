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

def unzip_file(filename, target_directory):

    print(f'Unzipping {filename} to {target_directory}')

    os.makedirs(target_directory, exist_ok=True)
    with zipfile.ZipFile(filename, 'r') as zip_ref:
        file_list = zip_ref.namelist()
        total_files = len(file_list)
        extracted_count = 0

        for file_name in file_list:
            extracted_count += 1

            print(f'Extracting: {file_name} ({extracted_count}/{total_files})', end='\r')
            sys.stdout.flush()

            zip_ref.extract(file_name, target_directory)
        
        print('\nUnzipping complete.')
    
    os.remove(filename)
    print(f'Zip file {filename} deleted.')

# Download EgoMusic from Zenodo
url = 'https://zenodo.org/records/16753794/files/EgoMusic.zip'
filename = 'EgoMusic.zip'
download_file(url, filename)

# Unzip downloaded file and remove the zip file.
target_directory = '.'
unzip_file(filename, target_directory)
