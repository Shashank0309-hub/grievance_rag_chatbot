import time
from starlette.requests import Request
from loguru import logger
from starlette.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR

from app.core.config import VERSION, EnvConfigs
from app.core.events import create_start_app_handler, create_stop_app_handler
from app.api.routes.api import router as api_router


def get_application() -> FastAPI:
    application = FastAPI(
        title=EnvConfigs.SERVICE_NAME,
        version=VERSION,
        openapi_prefix=EnvConfigs.OPENAPI_PREFIX,
    )

    application.add_event_handler("startup", create_start_app_handler(application))
    application.add_event_handler("shutdown", create_stop_app_handler(application))

    application.include_router(api_router)

    @application.middleware("http")
    async def add_process_time_header(request: Request, call_next):
        try:
            start_time = time.time()
            response = await call_next(request)
            process_time = round(round((time.time() - start_time) * 1000, 2))
            response.headers["X-Process-Time"] = str(process_time) + " ms"
            logger.info("{0} took time {1} ms", request.url.path, process_time)
            return response

        except Exception as exc:
            logger.exception(exc)
            return JSONResponse(
                {
                    "message": "Internal Server Error",
                    "status": HTTP_500_INTERNAL_SERVER_ERROR,
                },
                status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            )

    application.add_middleware(
        CORSMiddleware,
        allow_origins=EnvConfigs.ALLOWED_HOSTS or ["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return application


app = get_application()
