from pydantic import BaseModel, EmailStr, ConfigDict, field_serializer, Field
from pydantic_mongo import PydanticObjectId
from datetime import datetime

from typing import Optional, Any

class BaseResponse(BaseModel):
    @field_serializer('expiry_date', 'insert_date', check_fields=False)
    def serialize_dt(self, dt: datetime, _info):
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    
    @field_serializer('id', '_id', check_fields=False)
    def serialize_object_id(self, obj_id: Any, _info):
        return str(obj_id)

'''
models related to Item
'''
class Item(BaseModel):
    name: str
    email: EmailStr
    item_name: str
    quantity: int
    expiry_date: datetime

class ItemUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    item_name: Optional[str] = None
    quantity: Optional[int] = None
    expiry_date: Optional[datetime] = None

class ItemResponse(BaseResponse, Item):
    insert_date: datetime
    _id: Optional[PydanticObjectId] = None
    id: Optional[PydanticObjectId] = Field(alias="_id")



'''
models related to ClockIn
'''
class ClockIn(BaseModel):
    email: EmailStr
    location: str

class ClockInUpdate(BaseModel):
    email: Optional[EmailStr] = None
    location: Optional[str] = None

class ClockInResponse(BaseResponse, ClockIn):
    insert_date: datetime
    _id: Optional[PydanticObjectId] = None
    id: Optional[PydanticObjectId] = Field(alias="_id")
