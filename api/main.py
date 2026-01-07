from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from youtube_transcript_api import YouTubeTranscriptApi
# Make sure your summarizer import matches your folder structure:
from summarizer.summarize import summarize_transcript

app = FastAPI()

# 1. ALLOW CHROME EXTENSION TO TALK TO API (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://www.youtube.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. DEFINE INPUT FORMAT (Must match what content.js sends)
class VideoRequest(BaseModel):
    video_id: str

# 3. HELPER: FETCH TRANSCRIPT FROM YOUTUBE
def fetch_transcript_text(video_id: str) -> str:
    try:
        ytt_api = YouTubeTranscriptApi()
        transcript_list = ytt_api.fetch(video_id)
        # Join the list of text fragments into one long string
        full_text = " ".join([item.text for item in transcript_list])
        return full_text
    except Exception as e:
        print(f"Error fetching transcript: {e}")
        raise HTTPException(status_code=400, detail="Could not fetch transcript. Video might not have captions.")

# 4. API ENDPOINT
@app.post("/summarize")
def summarize(request: VideoRequest):
    print(f"✅ Connection received! Processing Video ID: {request.video_id}")
    
    # A. Get the text
    transcript_text = fetch_transcript_text(request.video_id)
    print(f"   - Transcript found ({len(transcript_text)} chars). Summarizing...")
    
    # B. Summarize it (Using your existing LLM function)
    summary_text = summarize_transcript(transcript_text)
    
    return {"summary": summary_text}