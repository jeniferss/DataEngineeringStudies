import os

from dotenv import load_dotenv


load_dotenv()

AWS_ACCESS_KEY_ID = os.getenv('BULK_AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('BULK_AWS_SECRET_ACCESS_KEY')
AWS_SESSION_TOKEN = os.getenv('BULK_AWS_SESSION_TOKEN')
AWS_REGION = os.getenv('BULK_AWS_REGION')
BUCKET_NAME = 'js-s3files'
