import re

def normalize_transcript(text: str) -> str:
    # Replace newlines with spaces
    text = text.replace("\n", " ")

    # Collapse multiple spaces
    text = re.sub(r"\s+", " ", text)

    # Remove timestamps in the format [00:00] or (00:00)
    text = re.sub(r"\b\d{1,2}:\d{2}\b", "", text)

    return text.strip()