from datetime import datetime
from bson.objectid import ObjectId
from pymongo.collection import Collection


def insert_workout(collection_mongo: Collection, telegram_id: int, data: dict):

    collection_mongo.insert_one(
        {
            "telegram_id": telegram_id,
            "time": datetime.now(),
            "train": data,
        }
    )
