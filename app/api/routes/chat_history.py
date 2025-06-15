from fastapi import APIRouter, Depends
from typing import List, Union

from app.api.dependencies.chat_history import post_chat_history, get_chat_history
from app.schemas.chat import ChatHistoryResponse

router = APIRouter(prefix="/v1/chat_history", tags=["ChatHistory"])


@router.post("/", response_model=dict)
async def post_chat_history(response=Depends(post_chat_history)):
    return response


@router.get("/{session_id}", response_model=Union[List[ChatHistoryResponse], None])
async def get_chat_history(response=Depends(get_chat_history)):
    return response
