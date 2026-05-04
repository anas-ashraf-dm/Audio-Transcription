import os

from fastapi import FastAPI

from app.config import TRANSCRIPT_DIR, UPLOAD_DIR
from app.router import router

app = FastAPI(title="Transcription POC")

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(TRANSCRIPT_DIR, exist_ok=True)

app.include_router(router)


@app.get("/health")
def health():
    return {"status": "running"}
