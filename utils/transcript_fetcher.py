from youtube_transcript_api import YouTubeTranscriptApi

def fetch_transcript(youtube_url):
    try:
        video_id = youtube_url.split("v=")[-1]
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        full_text = " ".join([item['text'] for item in transcript_list])
        return full_text
    except Exception as e:
        return f"Error fetching transcript: {e}"