import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
SECRET_KEY = os.getenv("SECRET_KEY", "default_key")
ALGORITHM = os.getenv("ALGORITHM", "default_algorithm")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "default_api_key")

ACCESS_TOKEN_EXPIRE_MINUTES = 120


def _as_bool(value: str | None, default: bool = False) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


ENABLE_MATCHED_POSITIONS = _as_bool(os.getenv("ENABLE_MATCHED_POSITIONS"), default=False)
