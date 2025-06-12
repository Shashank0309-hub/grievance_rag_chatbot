from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings

VERSION = "1.0.0"

config = Config(".env")

class EnvConfigs:
    SERVICE_NAME: str = config("SERVICE_NAME", cast=str, default="Grievance Rag Chatbot")
    OPENAPI_PREFIX: str = config("OPENAPI_PREFIX", default='')
    ALLOWED_HOSTS: CommaSeparatedStrings = config(
        "ALLOWED_HOSTS", cast=CommaSeparatedStrings, default=["*"]
    )
    LLM_API_KEY: str = config("LLM_API_KEY", cast=str, default=None)
    LLM_MODEL: str = config("LLM_MODEL", cast=str, default=None)
    MONGO_CONN_STR: str = config("MONGO_CONN_STR", cast=str, default=None)
