import requests
import os
from datetime import datetime
from dotenv import load_dotenv, set_key

# Load variables from the .env file
load_dotenv()

# Get the environment variables
url = os.getenv("CSV_URL")
# Use the relative path defined in .env for SAVE_DIRECTORY
save_directory = os.getenv("SAVE_DIRECTORY", os.path.join(os.getcwd(), 'data', 'CSV_Files'))  # Default to relative path if not defined

# Generate the file name and save in the relative CSV Files directory
save_path = os.path.join(save_directory, f"dboUnificado_{datetime.now().strftime('%Y-%m-%d')}.csv")

def download_csv(url, save_path):
    print('Making GET petition to the specified URL...')
    response = requests.get(url)
    if response.status_code == 200:
        print('Petition Successful! downloading info and creating file...')
        
        # Ensure the directory exists
        os.makedirs(save_directory, exist_ok=True)
        
        with open(save_path, 'wb') as file:
            file.write(response.content)
        print(f"File downloaded at {save_path}")
        
        # Update the .env file with the new CSV_FILE path (relative)
        relative_csv_file_path = os.path.relpath(save_path, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        env_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
        set_key(env_file, 'CSV_FILE', relative_csv_file_path)
        print(f'Updated CSV_FILE in .env to: {relative_csv_file_path}')
        
    else:
        print("Failed to download file")

download_csv(url, save_path)