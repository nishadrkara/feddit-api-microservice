import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    FEDDIT_KEY = os.environ['FEDDIT_URL']
