# Transcription POC

FastAPI server for audio transcription with speaker diarization using faster-whisper and pyannote, running on an Azure NC4as T4 v3 GPU VM.

---

## Setup

**1. Install uv** (if not already installed):
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**2. Create virtualenv and install dependencies:**
```bash
uv sync
```

**3. Set your Hugging Face token** in [app/config.py](app/config.py):
```python
HF_TOKEN = "hf_your_token_here"
```

**4. Accept the pyannote license** before first run:
- Visit https://hf.co/pyannote/speaker-diarization-3.1 and accept the terms

---

## Run

```bash
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

---

## Test

**Health check:**
```bash
curl http://localhost:8000/health
```

**Upload an audio file:**
```bash
curl -X POST http://localhost:8000/transcribe \
  -F "file=@/path/to/audio.mp3"
```

---

## Expected Output

**JSON response:**
```json
{
  "status": "success",
  "message": "Transcription complete",
  "transcript_saved_at": "transcripts/audio.mp3.txt"
}
```

**Transcript file format (`transcripts/audio.mp3.txt`):**
```
[0.0 - 3.4] SPEAKER_00: Hello, welcome to the meeting.
[3.5 - 7.1] SPEAKER_01: Thanks for having me.
[7.2 - 12.0] SPEAKER_00: Let's get started.
```

---

## Notes

- Models load once at startup — the first request after boot will be slow while GPU memory is populated
- The `/transcribe` endpoint is synchronous; the HTTP request blocks until transcription completes
- Transcripts are saved as plain `.txt` files in `transcripts/`
- Uploaded files are saved to `uploads/`
