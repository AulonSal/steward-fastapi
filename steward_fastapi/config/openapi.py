"""OpenAPI-schema"""
from steward_fastapi.config.base import BaseSettings

OPENAPI_API_NAME = "Steward - AulonSal"
OPENAPI_API_VERSION = "0.0.1 beta"
OPENAPI_API_DESCRIPTION = "Personal Steward Api"


class OpenAPISettings(BaseSettings):
    name: str
    version: str
    description: str

    @classmethod
    def generate(cls):
        return OpenAPISettings(
            name=OPENAPI_API_NAME,
            version=OPENAPI_API_VERSION,
            description=OPENAPI_API_DESCRIPTION,
        )
