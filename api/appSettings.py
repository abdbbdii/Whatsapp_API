import os
from .models import Settings
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv()) if not os.getenv("VERCEL_ENV") else None
appSettings = Settings.load()
