from dotenv import load_dotenv
from pydantic_settings import BaseSettings

#loads the values to environment variables
load_dotenv()

class Settings(BaseSettings):
    #gets the below from environment variables
    MONGO_DB_URL: str
    MONGO_DB_NAME: str
    OLLAMA_URL: str
    OLLAMA_MODELS: str

    #if the variables are not set above, it will get the env file
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"