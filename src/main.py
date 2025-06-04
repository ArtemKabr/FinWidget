# src/main.py
from fastapi import FastAPI

from src.views import router

app = FastAPI()
app.include_router(router)
