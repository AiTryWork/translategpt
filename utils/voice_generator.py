import os
import requests
from dotenv import load_dotenv

# ✅ Load env in case it's not already loaded
dotenv_path = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(dotenv_path)

def generate_voice(text):
    api_key = os.getenv("ELEVENLABS_API_KEY")
    voice_id = os.getenv("ELEVENLABS_VOICE_ID")

    print("🔑 ElevenLabs API Key:", api_key)
    print("🎙️ Voice ID:", voice_id)

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {
        "xi-api-key": api_key,
        "Content-Type": "application/json"
    }
    json = {
        "text": text[:4900],  # Trim in case it's too long
        "voice_settings": {
            "stability": 0.75,
            "similarity_boost": 0.75
        }
    }

    response = requests.post(url, headers=headers, json=json)

    if response.status_code != 200:
        print("🧨 ElevenLabs ERROR:", response.status_code)
        print("💬 Response Text:", response.text)
        raise Exception("Voice generation failed")

    output_path = "output.mp3"
    with open(output_path, "wb") as f:
        f.write(response.content)

    return output_path
