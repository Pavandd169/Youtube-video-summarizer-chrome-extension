from transformers import pipeline

def load_summarizer():
    return pipeline(
        "summarization",
        model="facebook/bart-large-cnn",
        device=-1  # CPU
    )