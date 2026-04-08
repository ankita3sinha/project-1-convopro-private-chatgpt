from pymongo import MongoClient
from config.settings import Settings

settings = Settings()

#connect to Mongo DB
_client = MongoClient(settings.MONGO_DB_URL, tz_aware=True)
#connect to the particular database
_db = _client[settings.MONGO_DB_NAME]

def get_collection(name: str):
    return _db[name]