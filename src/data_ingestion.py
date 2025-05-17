import os
import pandas 
from google.cloud import storage
from sklearn.model_selection import train_test_split
from src.logger import get_logger
from src.custom_exception import CustomException
from config.paths_config import *
from utils.common_functions import read_yaml
from dotenv import load_dotenv


# Load .env file at the beginning of your script
load_dotenv()

logger = get_logger(__name__)

class DataIngestion:
    def __init__(self, config):
        self.config = config["data_ingestion"]
        self.bucket_name = self.config["bucket_name"]
        self.file_name = self.config["bucket_file_name"]
        self.train_test_ratio = self.config["train_ratio"]
        self.credentials_path = os.environ.get('GCP_CREDENTIALS_PATH')
        if not self.credentials_path:
             logger.warning("GCP_CREDENTIALS_PATH environment variable not found. Make sure your .env file is correctly set up.")
        self.scopes = os.environ.get('GCP_SCOPES')
        os.makedirs(RAW_DIR, exist_ok=True)
        logger.info(f"Data Ingestion started with {self.bucket_name} and file is {self.file_name}")

    def download_csv_from_gcp(self):
        try:
            from google.oauth2 import service_account
        
            # Explicit path to your service account file
            # credentials_path = r"C:\Users\USER\Desktop\code\GCP-LL\personal\powerful-genre-457909-p3-554b3e67e3de.json"
            credentials_path = self.credentials_path
       
        
            # Log file existence check
            if not os.path.exists(credentials_path):
              raise FileNotFoundError(f"Credentials file not found at: {credentials_path}")
            logger.info(f"Found credentials file at: {credentials_path}")
        
            # Create credentials object
            credentials = service_account.Credentials.from_service_account_file(
              credentials_path, 
              scopes=[self.scopes]
            )
        
            # Create client with explicit credentials
            client = storage.Client(
              project=credentials.project_id,
              credentials=credentials
            )
        
            logger.info(f"Successfully authenticated to project: {credentials.project_id}")
        
            # Access bucket and file
            bucket = client.bucket(self.bucket_name)
            blob = bucket.blob(self.file_name)
            blob.download_to_filename(RAW_FILE_PATH)
            logger.info(f"Raw file is successfully downloaded to {RAW_FILE_PATH}")
            # client = storage.Client()
            # print(client)
            # bucket = client.bucket(self.bucket_name)
            # blob = bucket.blob(self.file_name)
            # blob.download_to_filename(RAW_FILE_PATH)
            # logger.info(f"Raw file is successfully downloaded to {RAW_FILE_PATH}")

        except Exception as e:
            logger.error(f"Error while downloading the csv file: {type(e).__name__}: {str(e)}")
            # Pass the exception object directly
            raise CustomException("Failed to download csv file", e)
        
    def split_data(self):
        try:
            logger.info("Starting the plitting the process")
            data = pandas.read_csv(RAW_FILE_PATH)
            train_data, test_data = train_test_split(data, test_size=1-self.train_test_ratio, random_state=42)

            train_data.to_csv(TRAIN_FILE_PATH)
            test_data.to_csv(TEST_FILE_PATH)
            logger.info(f"Train data is saved to {TRAIN_FILE_PATH}")
            logger.info(f"Test data is saved to {TEST_FILE_PATH}")
           
        except Exception as e:
            logger.error("Error while splitting the data")
            raise CustomException("Failed to split the data into training and testing sets", e)
        

    def run(self):
        try:
            logger.info("Starting the data ingestion process")
            self.download_csv_from_gcp()
            self.split_data()
            logger.info("Data ingestion process completed successfully")
        except Exception as ce:
            logger.error(f"Custom Exception: {str(ce)}")
           
            
        finally:
            logger.info("Data ingestion process completed")

if __name__ == "__main__":
    data_ingestion = DataIngestion(read_yaml(CONFIG_PATH))
    data_ingestion.run()
            