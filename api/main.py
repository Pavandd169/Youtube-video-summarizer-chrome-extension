from fastapi import FastAPI
from pydantic import BaseModel
from summarizer.summarize import summarize_transcript

app = FastAPI(
    title="YouTube Video Summarizer",
    description="Local - LLM-powered transcript summarization service",
    version="1.0"
)

class TranscriptRequest(BaseModel):
    transcript: str

class SummaryResponse(BaseModel):
    summary: str

@app.post("/summarize", response_model=SummaryResponse)
def summarize(request: TranscriptRequest):
    summary = summarize_transcript(request.transcript)
    return SummaryResponse(summary=summary)