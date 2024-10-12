from fastapi import HTTPException
from pymongo import MongoClient
from bson import ObjectId
from app.models import Item, ClockIn
from typing import List, Optional
from datetime import datetime
import os

MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017")
DATABASE_NAME = os.environ.get("DATABASE_NAME", "trackit")

def string_to_date(date_str: str) -> datetime:
    formats = [
        '%Y-%m-%d %H:%M:%S',
        '%Y-%m-%d',
    ]
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    
    raise HTTPException(
        status_code=400,
        detail=f"Date '{date_str}' does not match any expected format."
    )

class CRUDBase:
    def __init__(self, collection_name: str):
        self.client = MongoClient(MONGO_URI)
        self.db = self.client[DATABASE_NAME]
        self.collection_name = collection_name
        if not self.test_db_connection():
            raise HTTPException(status_code=500, detail="Database connection failed!")

    def test_db_connection(self):
        try:
            self.db.list_collection_names()
            return True
        except Exception:
            return False

    def create(self, item: dict) -> dict:
        item['insert_date'] = datetime.now()
        result = self.db[self.collection_name].insert_one(item)
        return str(result.inserted_id)

    def get_by_id(self, item_id: str) -> Optional[dict]:
        return self.db[self.collection_name].find_one({"_id": ObjectId(item_id)})

    def delete(self, item_id: str) -> bool:
        result = self.db[self.collection_name].delete_one({"_id": ObjectId(item_id)})
        return result.deleted_count > 0

    def update(self, item_id: str, updated_item: dict) -> Optional[dict]:
        self.db[self.collection_name].update_one({"_id": ObjectId(item_id)}, {"$set": updated_item})
        print("Updated")
        return self.get_by_id(item_id)

    def find(self, query: dict) -> List[dict]:
        return list(self.db[self.collection_name].find(query))  
    
    def _aggregate(self, pipeline: List) -> List:
        return list(self.db[self.collection_name].aggregate(pipeline))
    
    def group_by_email(self):
        pipeline = [
            {
                "$group": {
                    "_id": "$email",
                    "count": {"$sum": 1}
                }
            }
        ]
        data = self._aggregate(pipeline)
        return {each["_id"] : each["count"] for each in data}


class CRUDItems(CRUDBase):
    def __init__(self):
        super().__init__("items")

    def filter_items(self, email: Optional[str] = None, expiry_date: Optional[str] = None,
                     insert_date: Optional[str] = None, quantity: Optional[int] = None) -> List[Item]:
        query = {}
        if email:
            query["email"] = email
        if expiry_date:
            query["expiry_date"] = {"$gt": string_to_date(expiry_date)}
        if insert_date:
            query["insert_date"] = {"$gt": string_to_date(insert_date)}
        if quantity is not None:
            query["quantity"] = {"$gte": quantity}

        print(query)
        if query:
            items_data = self.find(query)
            return items_data
        else:
            raise HTTPException(
                status_code=400,
                detail="At least one parameter is required (email, expiry_date, insert_date, or quantity)."
            )


class CRUDClockIn(CRUDBase):
    def __init__(self):
        super().__init__("clock_in")

    def filter_clock_ins(self, email: Optional[str] = None, location: Optional[str] = None,
                          insert_datetime: Optional[str] = None) -> List[ClockIn]:
        query = {}
        if email:
            query["email"] = email
        if location:
            query["location"] = location
        if insert_datetime:
            query["insert_datetime"] = {"$gt": insert_datetime}

        if query:
            clockin_records = self.find(query)
            return clockin_records
        else:
            raise HTTPException(
                status_code=400,
                detail="At least one parameter is required (email, location, or insert_date)."
            )