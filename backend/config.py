import os
from dotenv import load_dotenv

load_dotenv()
SERP_API_KEY = os.getenv("SERP_API_KEY", "")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data/jobs.db")
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
PORT = int(os.getenv("PORT", 8000))
