from enum import Enum
from typing import List, Dict, Union, Optional

from pydantic import BaseModel


class ChatHistoryRequest(BaseModel):
    session_id: str
    messages: List[Dict[str, Union[str, None]]]

class ChatHistoryResponse(ChatHistoryRequest):
    created_at: str

class IntentModel(str, Enum):
    file_complaint = "file_complaint"
    check_status = "check_status"

class ChatIntentResponse(BaseModel):
    intent: IntentModel
    complaint_id: Optional[str] = None
    complaint_description: Optional[str] = None
    response: Optional[str] = None
    more_info_required: Optional[bool] = False
