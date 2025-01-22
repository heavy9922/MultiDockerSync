from fastapi import FastAPI
from app.routers import containers
app = FastAPI(title="Docker API Consolidator", version="1.0.0")

app.include_router(containers.router)
