import uuid
from typing import Optional

from loguru import logger
from starlette import status
from starlette.exceptions import HTTPException

from app.db.mongo_operations import grievance_db
from app.schemas.complaints import ComplaintRequest, ComplaintStatus, ComplaintResponse
from app.utils.grievance import GrievanceUtils


async def create_complaint(complaint: ComplaintRequest) -> dict:
    complaint_data = complaint.model_dump()
    complaint_id = await GrievanceUtils().generate_complaint_id()

    complaint_data.update({
        "_id": complaint_id,
        "name": complaint_data.get("name", "").strip().lower(),
        "mobile_number": complaint_data.get("mobile_number", "").strip().lower(),
        "status": ComplaintStatus.OPEN.value,
    })

    try:
        await grievance_db.create_complaint(complaint_data)
        logger.info(f"Complaint {complaint_id} created successfully for {complaint_data['name']}")
        return {"message": f"Complaint created successfully. Your complaint ID is {complaint_id}"}

    except Exception as e:
        logger.exception(f"Failed to create complaint: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while creating the complaint. Please try again later."
        )


async def get_complaint(complaint_id: Optional[str] = None, session_id: Optional[str] = None, mobile_number: Optional[str] = None):
    complaint = await grievance_db.get_complaint(complaint_id, session_id, mobile_number)

    if complaint and isinstance(complaint, dict) and complaint != {}:
        return ComplaintResponse(**complaint)

    return None
