from datetime import datetime
from typing import Dict, Optional, Any
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database
from app.core.config import EnvConfigs

class GrievanceDB:
    def __init__(self):
        self.client: MongoClient = MongoClient(EnvConfigs.MONGO_CONN_STR)
        self.db: Database = self.client["grievance_db"]
        self.complaints_collection: Collection = self.db["complaints"]
        self.chat_history_collection: Collection = self.db["chat_history"]
        self.session_collection: Collection = self.db["session"]

    async def create_complaint(self, complaint_data: Dict[str, Any]) -> str:
        result = self.complaints_collection.insert_one(complaint_data)
        if result.inserted_id:
            return str(result.inserted_id)
        raise Exception("Failed to create complaint")
    
    async def get_complaint(self, complaint_id: Optional[str] = None, session_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
        if session_id:
            return self.complaints_collection.find({"session_id": session_id})
        if complaint_id:
            return self.complaints_collection.find_one({"_id": complaint_id})
        raise ValueError("Either complaint_id or session_id must be provided")

    async def create_chat_history(self, chat_history: Dict[str, Any]) -> str:
        chat_history["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        result = self.chat_history_collection.insert_one(chat_history)
        if result.inserted_id:
            return str(result.inserted_id)
        raise Exception("Failed to create chat history")

    async def get_chat_history(self, session_id: str):
        return self.chat_history_collection.find({"session_id": session_id})

    async def add_session(self, session_data: Dict[str, Any]) -> str:
        session_exist = await self.get_session(session_data["session_id"])
        if session_exist:
            raise Exception("Session already exists")

        result = self.session_collection.insert_one(session_data)
        if result.inserted_id:
            return str(result.inserted_id)
        raise Exception("Failed to create session")

    async def get_session(self, session_id: str):
        return self.session_collection.find_one({"session_id": session_id})

    def close(self):
        self.client.close()

grievance_db = GrievanceDB()
