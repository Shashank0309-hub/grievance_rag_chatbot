from fastapi import APIRouter

from app.api.routes import customer, grievance, chat_history, session

router = APIRouter()

router.include_router(customer.router, tags=["Customer"])
router.include_router(grievance.router, tags=["Grievance"])
router.include_router(chat_history.router, tags=["ChatHistory"])
router.include_router(session.router, tags=["Session"])
