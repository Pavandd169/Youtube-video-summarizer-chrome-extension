from .model import load_summarizer
from .chunker import chunk_text
from .preprocess import normalize_transcript

summarizer = load_summarizer()

def summarize_transcript(text):
    text = normalize_transcript(text)

    ## If the text is too short, return it as is
    if len(text.split()) < 50:
        return text

    chunks = chunk_text(text)
    summaries = []

    for chunk in chunks:
        out = summarizer(
            chunk,
            max_length=120,
            min_length=30,
            do_sample=False
        )
        summaries.append(out[0]["summary_text"])

    if len(summaries) == 0:
        return ""
    if len(summaries) == 1:
        return summaries[0]
    
    # Final reduction
    final = summarizer(
        " ".join(summaries),
        max_length=300,
        min_length=50,
        do_sample=False
    )

    return final[0]["summary_text"]