from typing import Callable

from fastapi import FastAPI
from loguru import logger

from app.llm import llm_store_async


def create_start_app_handler(app: FastAPI) -> Callable:
    async def start_app() -> None:
        # await _initiate_aio_session()
        # await connect_to_mongo()
        # elastic.initiate_elastic(EnvElastic.PROVIDER)
        # await authenticator.get_jwks()
        await llm_store_async.initiate_llm()

    return start_app


def create_stop_app_handler(app: FastAPI) -> Callable:
    @logger.catch
    async def stop_app() -> None:
        # await _close_aio_session()
        # await close_mongo_connection()
        # await elastic.client.close()
        pass

    return stop_app
