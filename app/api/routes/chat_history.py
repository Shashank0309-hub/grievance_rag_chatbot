from fastapi import APIRouter, Depends
from typing import List, Union

from app.api.dependencies.chat_history import post_chat_history, get_chat_history
from app.schemas.chat import ChatHistoryRequest, ChatHistoryResponse

router = APIRouter(prefix="/v1/chat_history", tags=["ChatHistory"])


@router.post("/", response_model=dict)
async def create_complaint(response=Depends(post_chat_history)):
    return response


@router.get("/{complaint_id}", response_model=Union[List[ChatHistoryResponse], None])
async def get_complaint(response=Depends(get_chat_history)):
    return response
