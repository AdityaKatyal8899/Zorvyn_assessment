import os
from pathlib import Path

from dotenv import load_dotenv


# Load .env from the backend folder (development convenience)
BASE_DIR = Path(__file__).resolve().parents[2]
env_path = BASE_DIR / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=env_path)


def get_env(key: str, default: str = None) -> str:
    return os.environ.get(key, default)


# Application settings (access via import)
SQLALCHEMY_DATABASE_URL = get_env("SQLALCHEMY_DATABASE_URL", "sqlite:///./test.db")

