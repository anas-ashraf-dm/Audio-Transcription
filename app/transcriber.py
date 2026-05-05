import whisperx
from pyannote.audio import Pipeline

from app.config import COMPUTE_TYPE, DEVICE, HF_TOKEN, MODEL_SIZE, TRANSCRIPT_DIR

# Load models once at startup — never inside request handlers
model = whisperx.load_model(MODEL_SIZE, DEVICE, compute_type=COMPUTE_TYPE)
diarize_model = Pipeline.from_pretrained(
    "pyannote/speaker-diarization-3.1",
    token=HF_TOKEN,
).to(DEVICE)


def process_audio(audio_path: str, filename: str) -> str:
    audio = whisperx.load_audio(audio_path)

    # Transcribe
    result = model.transcribe(audio, batch_size=16)

    # Align for word-level timestamps
    align_model, metadata = whisperx.load_align_model(
        language_code=result["language"], device=DEVICE
    )
    result = whisperx.align(
        result["segments"], align_model, metadata, audio, DEVICE
    )

    # Diarize and assign speakers
    diarize_segments = diarize_model(audio_path)
    result = whisperx.assign_word_speakers(diarize_segments, result)

    # Format transcript lines
    lines = []
    for seg in result["segments"]:
        speaker = seg.get("speaker", "UNKNOWN")
        start = round(seg["start"], 1)
        end = round(seg["end"], 1)
        text = seg["text"].strip()
        lines.append(f"[{start} - {end}] {speaker}: {text}")

    transcript_text = "\n".join(lines)
    output_path = f"{TRANSCRIPT_DIR}/{filename}.txt"

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(transcript_text)

    return output_path
