"""Config of application"""
from .database import CONFIG as TORTOISE_ORM
from .openapi import OpenAPISettings

OPENAPI = OpenAPISettings.generate()
