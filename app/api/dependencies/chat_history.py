from starlette.exceptions import HTTPException

from app.db.mongo_operations import grievance_db
from app.schemas.chat import ChatHistoryRequest, ChatHistoryResponse


async def post_chat_history(chat: ChatHistoryRequest):
    try:
        chat_id = await grievance_db.create_chat_history(chat.model_dump())
        return {"id": chat_id, "message": "Chat history saved successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save chat history: {e}")

async def get_chat_history(session_id: str):
    try:
        chat_history = await grievance_db.get_chat_history(session_id)
        if chat_history:
            chat_history = [ChatHistoryResponse(**item) for item in chat_history]
            return chat_history
        raise None
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching chat history: {e}")