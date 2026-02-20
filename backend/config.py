import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
SECRET_KEY = os.getenv("SECRET_KEY", "default_key")
ALGORITHM = os.getenv("ALGORITHM", "default_algorithm")

ACCESS_TOKEN_EXPIRE_MINUTES = 120