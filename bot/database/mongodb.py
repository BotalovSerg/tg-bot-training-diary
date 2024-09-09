from datetime import datetime
from bson.objectid import ObjectId
from pymongo.collection import Collection


def insert_workout(collection_mongo: Collection, telegram_id: int, data: dict) -> None:

    collection_mongo.insert_one(
        {
            "telegram_id": telegram_id,
            "time": datetime.now(),
            "train": data,
        }
    )


def get_all_workout(collection_mongo: Collection, telegram_id: int) -> dict:
    query = {"telegram_id": telegram_id}
    all_workout = collection_mongo.find(query, {"_id": 1, "time": 1, "train": 1}).sort(
        "time", -1
    )
    return all_workout
