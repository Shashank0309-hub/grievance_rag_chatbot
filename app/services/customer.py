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
    async def _dump_chat_history(session_id, query, chat_response):
        await post_chat_history(
            ChatHistoryRequest(
                session_id=session_id,
                messages=[
                    {"role": "user", "content": query},
                    {"role": "system", "content": chat_response}
                ]
            )
        )

    async def generate_answer(self, query: str, session_id: str):
        """
        1. gets query
        2. chatbot will check if name and mobile number is present in query
        3. if not present, it will prompt user to provide name and mobile number then add to database
        4. if present, it will check if name and mobile number is present in database
        5. then will generate the complaint by calling the right function and give the complaint id
        6. if user want to check for status of the complaint, it will check the status of the complaint by calling the right function
        """
        chat_response = None

        session_data = await get_session(session_id)
        if session_data:
            name = session_data.name
            mobile_number = session_data.mobile_number
        else:
            name, mobile_number, chat_response = await self._is_user_details_present(query)
            await self._dump_chat_history(session_id, query, chat_response)

        if not session_data and name and mobile_number:
            await add_session(Session(session_id=session_id, name=name, mobile_number=mobile_number))

        if name and mobile_number:
            chat_history = await get_chat_history(session_id)

            intent = await self._check_intent(query, chat_history)

            if intent.intent == IntentModel.file_complaint:
                if intent.more_info_required:
                    await self._dump_chat_history(session_id, query, intent.response)
                    return {"response": intent.response}

                chat_response = await create_complaint(
                    ComplaintRequest(
                        description=intent.complaint_description,
                        session_id=session_id,
                        name=name,
                        mobile_number=mobile_number
                    )
                )
                await self._dump_chat_history(session_id, query, chat_response['message'])
            elif intent.intent == IntentModel.check_status:
                complaint_details = await get_complaint(session_id=session_id)
                if complaint_details:
                    if not intent.complaint_id:
                        await self._dump_chat_history(session_id, query, intent.response)
                        return {"response": intent.response}

                    complaint_details = await get_complaint(complaint_id=intent.complaint_id)
                    chat_response = await self._complaint_response(complaint_details)

                    await self._dump_chat_history(session_id, query, chat_response)
                    return {"response": chat_response}
                else:
                    chat_response = "No complaints found for the given session."
                    await self._dump_chat_history(session_id, query, chat_response)
                    return {"response": chat_response}

        return {"response": chat_response}

    @staticmethod
    async def _is_user_details_present(query: str):
        user_prompt = USER_DETAILS_PROMPT.format(query=query)

        chat_response = await llm_store_async.mistral_ai.get_chat_response(
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "system", "content": user_prompt},
            ]
        )

        try:
            cleaned_response = chat_response.strip()

            if cleaned_response.startswith("```json") or cleaned_response.startswith("```"):
                cleaned_response = cleaned_response.strip("`").replace("json", "").strip()

            response = json.loads(cleaned_response)

            return response["name"], response["mobile_number"], response["response"]

        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {e}")
            raise ValueError("Invalid JSON format received from LLM.")

    @staticmethod
    async def _check_intent(user_query: str, chat_history: list, user_exists: bool = True) -> ChatIntentResponse:
        user_prompt = INTENT_PROMPT.format(user_query=user_query, chat_history=chat_history, user_exists=user_exists)

        chat_response = await llm_store_async.mistral_ai.get_chat_response(
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ]
        )

        try:
            cleaned_response = chat_response.strip()

            if cleaned_response.startswith("```json") or cleaned_response.startswith("```"):
                cleaned_response = cleaned_response.strip("`").replace("json", "").strip()

            cleaned_response = json.loads(cleaned_response)
            cleaned_response = ChatIntentResponse.model_validate(cleaned_response)
            return cleaned_response

        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {e}")
            raise ValueError("Invalid JSON format received from LLM.")

    @staticmethod
    async def _complaint_response(complaint_details: ComplaintResponse):
        prompt = COMPLAINT_RESPONSE_PROMPT.format(complaint_details=complaint_details.model_dump())

        chat_response = await llm_store_async.mistral_ai.get_chat_response(
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ]
        )

        try:
            cleaned_response = chat_response.strip()

            if cleaned_response.startswith("```json") or cleaned_response.startswith("```"):
                cleaned_response = cleaned_response.strip("`").replace("json", "").strip()

            cleaned_response = json.loads(cleaned_response)['response']
            return cleaned_response

        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {e}")
            raise ValueError("Invalid JSON format received from LLM.")
