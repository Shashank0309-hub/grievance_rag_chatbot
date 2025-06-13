import json
from loguru import logger

from app.api.dependencies.chat_history import post_chat_history, get_chat_history
from app.api.dependencies.grievance import create_complaint, get_complaint
from app.api.dependencies.session import get_session, add_session
from app.llm import llm_store_async
from app.schemas.chat import IntentModel, ChatHistoryRequest, ChatIntentResponse
from app.schemas.complaints import ComplaintRequest, ComplaintResponse
from app.schemas.session import Session
from app.utils.prompts import INTENT_PROMPT, USER_DETAILS_PROMPT, SYSTEM_PROMPT, COMPLAINT_RESPONSE_PROMPT


class CustomerService:
    @staticmethod
    async def _dump_chat_history(session_id, user_input, system_response):
        await post_chat_history(ChatHistoryRequest(
            session_id=session_id,
            messages=[
                {"role": "user", "content": user_input},
                {"role": "system", "content": system_response}
            ]
        ))

    async def generate_answer(self, query: str, session_id: str):
        query = query.lower()
        session = await get_session(session_id)
        name, mobile_number, chat_response = None, None, None

        if session:
            name, mobile_number = session.name, session.mobile_number
        else:
            name, mobile_number, chat_response = await self._extract_user_details(query)
            if chat_response:
                await self._dump_chat_history(session_id, query, chat_response)
            if name and mobile_number:
                await add_session(Session(session_id=session_id, name=name, mobile_number=mobile_number))

        if not (name and mobile_number):
            return {"response": chat_response}

        intent = await self._detect_intent(query, await get_chat_history(session_id))

        if intent.intent == IntentModel.file_complaint:
            if intent.more_info_required:
                await self._dump_chat_history(session_id, query, intent.response)
                return {"response": intent.response}

            chat_response = await create_complaint(ComplaintRequest(
                description=intent.complaint_description,
                session_id=session_id,
                name=name,
                mobile_number=mobile_number
            ))
            await self._dump_chat_history(session_id, query, chat_response["message"])
            return {"response": chat_response["message"]}

        elif intent.intent == IntentModel.check_status:
            if not intent.complaint_id:
                await self._dump_chat_history(session_id, query, intent.response)
                return {"response": intent.response}

            complaint = await get_complaint(complaint_id=intent.complaint_id, mobile_number=mobile_number)
            if not complaint:
                response = "Sorry but we didn't find any complaints for the given mobile number and ticket id."
                await self._dump_chat_history(session_id, query, response)
                return {"response": response}

            chat_response = await self._format_complaint_response(complaint)
            await self._dump_chat_history(session_id, query, chat_response)
            return {"response": chat_response}

        return {"response": chat_response or "I'm not sure how to help with that."}

    async def _extract_user_details(self, query: str):
        prompt = USER_DETAILS_PROMPT.format(query=query)
        response = await self._call_llm([
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "system", "content": prompt}
        ])
        return response.get("name"), response.get("mobile_number"), response.get("response")

    async def _detect_intent(self, user_query: str, chat_history: list) -> ChatIntentResponse:
        prompt = INTENT_PROMPT.format(user_query=user_query, chat_history=chat_history, user_exists=True)
        response = await self._call_llm([
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ])
        return ChatIntentResponse.model_validate(response)

    async def _format_complaint_response(self, complaint: ComplaintResponse):
        prompt = COMPLAINT_RESPONSE_PROMPT.format(complaint_details=complaint.model_dump())
        response = await self._call_llm([
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ])
        return response.get("response")

    async def _call_llm(self, messages: list) -> dict:
        try:
            raw = await llm_store_async.mistral_ai.get_chat_response(messages=messages)
            cleaned = self._clean_llm_response(raw)
            return json.loads(cleaned)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse LLM response: {e}")
            raise ValueError("Invalid JSON format received from LLM.")

    @staticmethod
    def _clean_llm_response(response: str) -> str:
        response = response.strip()
        if response.startswith("```"):
            response = response.strip("`").replace("json", "").strip()
        return response
