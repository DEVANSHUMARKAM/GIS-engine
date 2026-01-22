from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    ENV = os.getenv("ENV", "development")
    DEBUG = os.getenv("DEBUG", "False") == "True"

    MODEL_PATH = os.getenv("MODEL_PATH")
    CACHE_DIR = os.getenv("CACHE_DIR")

settings = Settings()
