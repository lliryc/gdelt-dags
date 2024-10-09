import requests
import io
import zipfile
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime
import io

def write_raw_gkg_content_to_db(url):
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
            
        for _, csv_content in extracted_content.items():
            # Create a list of column names from the SQL file
            columns = [
                'record_id', 'date_label', 'source_collection_id', 'source_common_name',
                'document_identifier', 'counts', 'counts_v2', 'themes', 'themes_enhanced',
                'locations', 'locations_enhanced', 'persons', 'persons_enhanced',
                'organizations', 'organizations_enhanced', 'tone', 'dates_enhanced',
                'gcam', 'sharing_image', 'related_images', 'social_image_embeds', 'social_video_embeds',
                'quotations', 'all_names', 'amounts', 'translation_info', 'extras_xml'
            ]

            # Read the CSV content into a pandas DataFrame
            df = pd.read_csv(io.StringIO(csv_content.decode("iso-8859-1")), dtype=str, sep='\t', header=None, names=columns)
          
            # Create the SQLAlchemy engine
            engine = create_engine('postgresql+psycopg2://airflow:airflow@postgres/gdelt')
            
            connection = engine.connect()

            # Remove rows where date_label is NA
            df = df.dropna(subset=['date_label'])

            df['date_dt'] = df['date_label'].apply(lambda x: datetime.strptime(x, '%Y%m%d%H%M%S'))

            df['trans_type'] = 'non-en' if 'translation' in url else 'en'
            
            # Save the DataFrame to the PostgreSQL table
            df.to_sql('gkg_raw', connection, schema='raw', if_exists='append', index=False)
            
            connection.close()

        return True
    
    else:
        print(f"Failed to download the file. Status code: {response.status_code}")
        return False

if __name__ == "__main__":
    # http://data.gdeltproject.org/gdeltv2/20150218224500.translation.gkg.csv.zip
    res = write_raw_gkg_content_to_db("http://data.gdeltproject.org/gdeltv2/20150218230000.gkg.csv.zip") 
    print(res)       

