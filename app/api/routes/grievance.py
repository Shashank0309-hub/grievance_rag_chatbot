from fastapi import APIRouter, Depends

from app.api.dependencies.grievance import create_complaint, get_complaint
from app.schemas.complaints import ComplaintResponse, ComplaintRequest

router = APIRouter(prefix="/v1/complaints", tags=["Grievance"])

@router.post("/", response_model=ComplaintRequest)
async def create_complaint(response = Depends(create_complaint)):
    return response


@router.get("/{complaint_id}", response_model=ComplaintResponse)
async def get_complaint(response = Depends(get_complaint)):
    return response

