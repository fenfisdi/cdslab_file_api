from fastapi import FastAPI

from src.db import MongoEngine
from src.routes import file_routes, folder_routes

db = MongoEngine().get_connection()
app = FastAPI()

app.include_router(folder_routes)
app.include_router(file_routes)
