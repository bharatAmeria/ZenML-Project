import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration class for the application."""
    DATA_URL = os.getenv("DATA_URL")
    DATA_FILE = os.getenv("DATA_FILE")
    LOG_DIR = "logs"

    @staticmethod
    def validate():
        """Validate that required environment variables are set."""
        if not Config.GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY is not set in the .env file")