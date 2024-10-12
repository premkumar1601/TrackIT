from fastapi import APIRouter, HTTPException, Header, Depends
from app.models import Item, ItemResponse, ItemUpdate
from app.crud import CRUDItems
from pydantic_mongo import PydanticObjectId
from typing import List, Optional
import os

from dotenv import load_dotenv
load_dotenv(dotenv_path="app.env")
API_KEY = os.environ.get("API_KEY", "mjx.D@Gv)2fi") 

def verify_api_key(api_key: str = Header(...)):
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return api_key

router = APIRouter(tags=["Items"], prefix="/items")
items = CRUDItems()

@router.post("/", response_model=dict, summary="Create an Item", description="Create a new item and return the created item.")
async def create_item(item: Item, api_key: str = Depends(verify_api_key)):
    item_data = item.model_dump()
    inserted_id = items.create(item_data)
    return {"inserted_id": inserted_id}

@router.get("/id/{item_id}", response_model=ItemResponse, summary="Get Item by ID", description="Retrieve an item by its ID.")
async def get_item(item_id: PydanticObjectId, api_key: str = Depends(verify_api_key)):
    item = items.get_by_id(item_id)
    print(item)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.get("/", response_model=List[ItemResponse], summary="Filter Items", description="Filter items based on any one optional query parameters such as email, expiry date, insert date, and quantity.")
async def filter_items(email: Optional[str] = None, 
                       expiry_date: Optional[str] = None,
                       insert_date: Optional[str] = None, 
                       quantity: Optional[int] = None,
                       api_key: str = Depends(verify_api_key)):
    result = items.filter_items(email=email, expiry_date=expiry_date,
                                     insert_date=insert_date, quantity=quantity)
    return result

@router.put("/id/{item_id}", response_model=ItemResponse, summary="Update Item", description="Update an existing item by its ID and return the updated item.")
async def update_item(item_id: PydanticObjectId, updated_item: ItemUpdate, api_key: str = Depends(verify_api_key)):
    print(updated_item)
    item_data = updated_item.model_dump(exclude_none=True)
    item = items.update(item_id, item_data)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.delete("/id/{item_id}", response_model=dict, summary="Delete Item", description="Delete an item by its ID.")
async def delete_item(item_id: PydanticObjectId, api_key: str = Depends(verify_api_key)):
    deleted = items.delete(item_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"detail": "Item deleted successfully"}


@router.get("/emails", response_model=dict, summary="Count of items for each email,")
async def group_emails(api_key: str = Depends(verify_api_key)):
    emails = items.group_by_email()
    return emails
