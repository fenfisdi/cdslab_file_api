from os import environ

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from src.config import fastApiConfig
from src.db import MongoEngine
from src.routes import (
    file_routes,
    folder_routes,
    root_routes,
    scrapping_routes
)

db = MongoEngine().get_connection()
app = FastAPI(**fastApiConfig)


app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=environ.get("ALLOWED_HOSTS", "*").split(",")
)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=environ.get("ALLOWED_ORIGINS", "*").split(","),
    allow_methods=environ.get("ALLOWED_METHODS", "*").split(","),
    allow_headers=environ.get("ALLOWED_HEADERS", "*").split(",")
)

app.include_router(folder_routes)
app.include_router(file_routes)
app.include_router(root_routes)
app.include_router(scrapping_routes)
