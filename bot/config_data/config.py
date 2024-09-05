import os
from dotenv import load_dotenv
from pydantic import BaseModel
from pydantic_settings import BaseSettings

load_dotenv()


class MongoDBConfig(BaseModel):
    url: str = os.getenv("MONGODB_URL")
    port: int = 27017
    NAME_DB: str = "BotFitnes"
    NAME_COLLECTION: str = "tranning"


class DataBaseConfig(BaseModel):
    url: str = os.getenv("PGDB_URL")
    echo: bool = False


class BotConfig(BaseModel):
    token: str = os.getenv("BOT_TOKEN")
    api_token_weather: str = os.getenv("API_KEY_OPEN_WEATHER")


class Settings(BaseSettings):
    mongo_db: MongoDBConfig = MongoDBConfig()
    bot: BotConfig = BotConfig()
    db: DataBaseConfig = DataBaseConfig()


settings = Settings()
