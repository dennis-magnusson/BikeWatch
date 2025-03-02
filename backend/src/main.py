import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .routes import alerts, listings

app = FastAPI(docs_url="/api/docs")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(listings.router, prefix="/api")
app.include_router(alerts.router, prefix="/api")

app.mount("/", StaticFiles(directory="/frontend", html=True), name="frontend")
