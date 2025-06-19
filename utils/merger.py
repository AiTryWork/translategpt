import os
import subprocess
import yt_dlp
import uuid

def merge_audio_with_video(youtube_url, audio_path):
    video_path = f"video_{uuid.uuid4().hex}.mp4"
    output_path = "translated_output.mp4"

    ydl_opts = {
        'format': 'best[ext=mp4][height<=360]/best',
        'outtmpl': video_path,
        'noplaylist': True,
        'quiet': False,
        'sleep_interval': 1.5,
        'max_sleep_interval': 3.0,
        'ratelimit': 512000,
        'throttled_rate': 256000,
    }

    print("⬇️ Downloading video to:", video_path)
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url])

    if not os.path.exists(video_path) or os.path.getsize(video_path) < 100000:
        raise Exception("❌ Video download failed or invalid (too small).")

    print("🎬 Merging voiceover with video using FFmpeg...")
    command = [
        "ffmpeg",
        "-y",
        "-i", video_path,
        "-i", audio_path,
        "-c:v", "copy",
        "-c:a", "aac",
        "-map", "0:v:0",
        "-map", "1:a:0",
        "-shortest",
        output_path
    ]

    subprocess.run(command, check=True)

    return output_path
