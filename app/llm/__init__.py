from app.llm.mistral_ai import MistralAILLMAsync


class LLMStoreAsync:
    mistral_ai: MistralAILLMAsync

    async def initiate_llm(
            self
    ):
        self.mistral_ai = MistralAILLMAsync()
        await self.mistral_ai.initiate_connection()

llm_store_async = LLMStoreAsync()