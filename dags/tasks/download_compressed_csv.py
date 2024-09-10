import requests
import io
import zipfile

def download_zip_content(url):
    # Define headers
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Content-Type': 'application/zip'
    }

    # Send a GET request to the URL with headers
    response = requests.get(url, headers=headers)
        # Check if the request was successful
    if response.status_code == 200:
        # Create a BytesIO object from the content
        zip_content = io.BytesIO(response.content)
        
        # Open the zip file
        with zipfile.ZipFile(zip_content, 'r') as zip_ref:
            # Extract all contents to memory
            extracted_content = {name: zip_ref.read(name) for name in zip_ref.namelist()}
        
        return extracted_content
    else:
        print(f"Failed to download the file. Status code: {response.status_code}")
        return None

# Example usage
url = "http://data.gdeltproject.org/gdeltv2/20150218230000.export.CSV.zip"
content = download_zip_content(url)

if content:
    for filename, file_content in content.items():
        print(f"File: {filename}, Size: {len(file_content)} bytes")
        with open(filename, 'wb') as f:
            f.write(file_content)
        