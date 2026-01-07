from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound, VideoUnavailable

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
        transcript_list = ytt_api.fetch(video_id, languages=['en', 'en-US', 'en-GB'])
        # Join the list of text fragments into one long string
        full_text = " ".join([item.text for item in transcript_list])
        return full_text
    
    except NoTranscriptFound:
        # Raised when the video exists, but no transcript in the requested language (English) matches
        raise HTTPException(status_code=404, detail="English captions are not available for this video.")
        
    except TranscriptsDisabled:
        # Raised when the video owner has disabled subtitles entirely
        raise HTTPException(status_code=403, detail="Subtitles are disabled for this video.")

    except VideoUnavailable:
        # Raised when the video ID is invalid or video is private
        raise HTTPException(status_code=404, detail="Video is unavailable or private.")
        
    except Exception as e:
        # Catch-all for connection errors or other issues
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

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