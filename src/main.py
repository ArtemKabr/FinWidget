from fastapi import FastAPI

from src.views import router as views_router

app = FastAPI()
app.include_router(views_router)
