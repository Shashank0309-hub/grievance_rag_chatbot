from fastapi import APIRouter, Depends
from starlette.status import HTTP_200_OK

from app.api.dependencies.customer import generate_answer
from app.api.routes.constants import Routes

router = APIRouter(prefix="/v1/customer", tags=["Customer"])

@router.get("/chat", name=Routes.CHAT, status_code=HTTP_200_OK)
async def get_answer(chat_response = Depends(generate_answer)):
    return chat_response