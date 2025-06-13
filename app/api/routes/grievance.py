from typing import Union

from fastapi import APIRouter, Depends

from app.api.dependencies.grievance import create_complaint, get_complaint, update_complaint_status
from app.schemas.complaints import ComplaintResponse, ComplaintRequest

router = APIRouter(prefix="/v1/complaints", tags=["Grievance"])


@router.post("/", response_model=ComplaintRequest)
async def create_complaint(response=Depends(create_complaint)):
    return response


@router.get("/{complaint_id}", response_model=Union[ComplaintResponse, None])
async def get_complaint(response=Depends(get_complaint)):
    return response


@router.patch("/{complaint_id}", response_model=dict)
async def update_complaint_status(response=Depends(update_complaint_status)):
    return response
