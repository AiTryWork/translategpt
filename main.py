import os
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from utils.transcript_fetcher import fetch_transcript
from utils.translator import translate_text
from utils.voice_generator import generate_voice
from utils.merger import merge_audio_with_video

app = FastAPI()

# ✅ Enable CORS for Netlify frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Optional: replace * with specific domain for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class VideoRequest(BaseModel):
    youtube_url: str
    target_language: str

@app.post("/process")
async def process_video(request: VideoRequest):
    try:
        print("📥 Request received for:", request.youtube_url)
        transcript = fetch_transcript(request.youtube_url)
        translated = translate_text(transcript, request.target_language)
        audio_path = generate_voice(translated)
        output_path = merge_audio_with_video(request.youtube_url, audio_path)
        print("✅ Video processed successfully. Output at:", output_path)
        return {"status": "success", "download_url": output_path}
    except Exception as e:
        print("❌ Error during processing:", str(e))
        return {"status": "error", "message": str(e)}
