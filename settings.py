from pydantic_settings import BaseSettings
from dotenv import find_dotenv
import os
from loguru import logger


class Settings(BaseSettings):
    OPENAI_API_KEY: str
    API_URL: str = "http://127.0.0.1:8000"

env_path = find_dotenv('.env')
settings = Settings(_env_file = env_path)

logger.info(f"Settings: {settings.model_dump_json()}")

os.environ.update(settings.model_dump())
