from datetime import datetime
from bson.objectid import ObjectId
from pymongo.collection import Collection
from pymongo.cursor import Cursor


def insert_workout(collection_mongo: Collection, telegram_id: int, data: dict) -> None:

    collection_mongo.insert_one(
        {
            "telegram_id": telegram_id,
            "time": datetime.now(),
            "train": data,
        }
    )


def get_all_workouts(collection_mongo: Collection, telegram_id: int) -> Cursor | None:
    query = {"telegram_id": telegram_id}
    if collection_mongo.count_documents(query):
        return collection_mongo.find(query, {"_id": 1, "time": 1, "train": 1}).sort("time", -1)
    return


def delete_workout(collection_mongo: Collection, _id: str):
    query = {"_id": ObjectId(_id)}
    result = collection_mongo.delete_one(query)

    return result.deleted_count
