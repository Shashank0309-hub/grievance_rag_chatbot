from typing import Callable

from fastapi import FastAPI
from loguru import logger

from app.db.mongo_operations import grievance_db
from app.llm import llm_store_async


def create_start_app_handler(app: FastAPI) -> Callable:
    async def start_app() -> None:
        await llm_store_async.initiate_llm()

    return start_app


def create_stop_app_handler(app: FastAPI) -> Callable:
    @logger.catch
    async def stop_app() -> None:
        grievance_db.close()

    return stop_app
