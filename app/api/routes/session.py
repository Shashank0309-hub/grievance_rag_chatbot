from typing import Union

from fastapi import APIRouter, Depends

from app.api.dependencies.session import add_session, get_session
from app.schemas.session import Session

router = APIRouter(prefix="/v1/session", tags=["Session"])


@router.post("/add_session", response_model=str)
async def add_session(response=Depends(add_session)):
    return response


@router.get("/{session_id}", response_model=Union[Session, None])
async def get_session(response=Depends(get_session)):
    return response
