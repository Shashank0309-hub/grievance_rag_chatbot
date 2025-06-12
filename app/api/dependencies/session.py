from starlette.exceptions import HTTPException

from app.db.mongo_operations import grievance_db
from app.schemas.session import Session


async def add_session(session: Session):
    try:
        await grievance_db.add_session(session.model_dump())
        return "Session added successfully"
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to add session: {e}")

async def get_session(session_id: str):
    try:
        session = await grievance_db.get_session(session_id)
        if session:
            return Session(**session)
        else:
            return None
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get session: {e}")