import os
import time
from pathlib import Path
from starlette.requests import Request
from fastapi.responses import FileResponse, HTMLResponse
from loguru import logger
from starlette.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR

from app.core.config import VERSION, EnvConfigs
from app.core.events import create_start_app_handler, create_stop_app_handler
from app.api.routes.api import router as api_router

# Get the base directory
BASE_DIR = Path(__file__).resolve().parent.parent


def get_application() -> FastAPI:
    application = FastAPI(
        title=EnvConfigs.SERVICE_NAME,
        version=VERSION,
        openapi_prefix=EnvConfigs.OPENAPI_PREFIX,
    )

    application.add_event_handler("startup", create_start_app_handler(application))
    application.add_event_handler("shutdown", create_stop_app_handler(application))

    application.include_router(api_router)
    
    # Get the absolute path to the project root
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    
    # Debug logging
    logger.info(f"Project root: {project_root}")
    logger.info(f"Project root contents: {os.listdir(project_root)}")
    
    # Mount the project root as static files
    static_dir = os.path.join(project_root, "static")
    application.mount("/static", StaticFiles(directory=static_dir), name="static")
    
    # Debug endpoint to check paths
    @application.get("/debug")
    async def debug():
        return {
            "project_root": project_root,
            "static_dir": static_dir,
            "static_dir_exists": os.path.exists(static_dir),
            "static_dir_contents": os.listdir(static_dir) if os.path.exists(static_dir) else [],
            "index_html_exists": os.path.exists(os.path.join(project_root, "index.html")),
            "cwd": os.getcwd()
        }
    
    # Serve the main page
    @application.get("/", response_class=HTMLResponse)
    async def read_root():
        index_path = os.path.join(project_root, "static/index.html")
        return FileResponse(index_path)

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
