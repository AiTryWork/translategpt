import os
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, Request
from pydantic import BaseModel
from utils.transcript_fetcher import fetch_transcript
from utils.translator import translate_text
from utils.voice_generator import generate_voice
from utils.merger import merge_audio_with_video
from fastapi.staticfiles import StaticFiles  # ✅ ADD THIS

app = FastAPI()

class VideoRequest(BaseModel):
    youtube_url: str
    target_language: str

@app.post("/process")
async def process_video(request: VideoRequest):
    try:
        transcript = fetch_transcript(request.youtube_url)
        translated = translate_text(transcript, request.target_language)
        audio_path = generate_voice(translated)
        output_path = merge_audio_with_video(request.youtube_url, audio_path)
        return {"status": "success", "download_url": output_path}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# ✅ ADD THIS AT THE END (after all route definitions)
app.mount("/", StaticFiles(directory="static", html=True), name="static")
