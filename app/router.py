import os
from fastapi import APIRouter, HTTPException, UploadFile
from app.config import UPLOAD_DIR
from app.transcriber import process_audio

router = APIRouter()

ALLOWED_EXTENSIONS = {".mp3", ".wav", ".m4a", ".mp4", ".ogg"}

@router.post("/transcribe")
async def transcribe(file: UploadFile):
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type '{ext}'. Allowed: {', '.join(ALLOWED_EXTENSIONS)}",
        )

    save_path = f"{UPLOAD_DIR}/{file.filename}"
    with open(save_path, "wb") as f:
        f.write(await file.read())

    try:
        transcript_path = process_audio(save_path, file.filename)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {
        "status": "success",
        "message": "Transcription complete",
        "transcript_saved_at": transcript_path,
    }
