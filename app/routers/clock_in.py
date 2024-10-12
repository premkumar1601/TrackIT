from fastapi import APIRouter, HTTPException, Header, Depends
from app.models import ClockIn, ClockInResponse, ClockInUpdate
from app.crud import CRUDClockIn
from typing import List, Optional
import os

API_KEY = os.environ.get("API_KEY", "123")

def verify_api_key(api_key: str = Header(...)):
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")

router = APIRouter(tags=["ClockIn"], prefix='/clockin')
clock_in_manager = CRUDClockIn()

@router.post("/", response_model=dict, summary="Create a Clock-In Entry", description="Create a new clock-in entry and return the created entry.")
async def create_clock_in(clock_in: ClockIn, api_key: str = Depends(verify_api_key)):
    clock_in_data = clock_in.model_dump()
    inserted_id = clock_in_manager.create(clock_in_data)
    return {"inserted_id": inserted_id}

@router.get("/id/{clock_in_id}", response_model=ClockInResponse, summary="Get Clock-In Entry by ID", description="Retrieve a clock-in entry by its ID.")
async def get_clock_in(clock_in_id: str, api_key: str = Depends(verify_api_key)):
    clock_in = clock_in_manager.get_by_id(clock_in_id)
    if not clock_in:
        raise HTTPException(status_code=404, detail="Clock-in entry not found")
    return clock_in

@router.get("/", response_model=List[ClockInResponse], summary="Filter Clock-In Entries", description="Filter clock-in entries based on optional query parameters such as email, location, and insert date.")
async def filter_clock_ins(email: Optional[str] = None, 
                            location: Optional[str] = None,
                            insert_datetime: Optional[str] = None,
                            api_key: str = Depends(verify_api_key)):
    clock_ins = clock_in_manager.filter_clock_ins(email=email, location=location, insert_datetime=insert_datetime)
    return clock_ins

@router.put("/id/{clock_in_id}", response_model=ClockInUpdate, summary="Update Clock-In Entry", description="Update an existing clock-in entry by its ID and return the updated entry.")
async def update_clock_in(clock_in_id: str, updated_clock_in: ClockInUpdate, api_key: str = Depends(verify_api_key)):
    clock_in_data = updated_clock_in.model_dump(exclude_none=True)
    updated_entry = clock_in_manager.update(clock_in_id, clock_in_data)
    if not updated_entry:
        raise HTTPException(status_code=404, detail="Clock-in entry not found")
    return updated_entry

@router.delete("/id/{clock_in_id}", response_model=dict, summary="Delete Clock-In Entry", description="Delete a clock-in entry by its ID.")
async def delete_clock_in(clock_in_id: str, api_key: str = Depends(verify_api_key)):
    deleted = clock_in_manager.delete(clock_in_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Clock-in entry not found")
    return {"detail": "Clock-in entry deleted successfully"}

@router.get("/emails", response_model=dict, summary="Count of items for each email,")
async def group_emails(api_key: str = Depends(verify_api_key)):
    emails = clock_in_manager.group_by_email()
    return emails