import time
from typing import List

from loguru import logger
from mistralai import Mistral

from app.core.config import EnvConfigs


class MistralAILLMAsync:
    client: Mistral

    async def initiate_connection(self):
        self.client = Mistral(api_key=EnvConfigs.LLM_API_KEY)
        logger.info("Mistral AI connection started")

    async def get_chat_response(
        self,
        messages: List[str],
        temperature=0.7,
    ):
        start_time = time.time()
        chat_response = await self.client.chat.complete_async(
            model=EnvConfigs.LLM_MODEL,
            messages=messages,
            temperature=temperature,
        )
        query_time = (time.time() - start_time) * 1000
        logger.info("took time {0} ms", round(round(query_time, 2)))

        return chat_response.choices[0].message.content