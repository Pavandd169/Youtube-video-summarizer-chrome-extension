from .model import ModelLoader
from .chunker import chunk_text
from .preprocess import normalize_transcript

def summarize_chunk(chunk, pipe):
    """Summarizes a single piece of text."""
    messages = [
        {"role": "system", "content": "You are a concise summarizer."},
        {"role": "user", "content": f"Summarize this text in 2-4 sentences:\n{chunk}"}
    ]
    
    # max_new_tokens limits the output length for speed
    result = pipe(messages, max_new_tokens=100, do_sample=False)
    return result[0]['generated_text'][-1]['content']

def generate_final_summary(combined_text, pipe):
    """Creates the final bulleted list from the chunk summaries."""
    messages = [
        {"role": "system", "content": "You are a helpful assistant. Formatting: Use Markdown bullet points."},
        {"role": "user", "content": (
            f"Here are the key points from a video:\n{combined_text}\n\n"
            "Create a final summary. Start with a short summary paragraph, "
            "then provide a list of few 'Key Takeaways' as bullet points."
        )}
    ]
    
    result = pipe(messages, max_new_tokens=300, temperature=0.3, do_sample=False) # sampling is off  
    return result[0]['generated_text'][-1]['content']

def summarize_transcript(text):
    text = normalize_transcript(text)

    ## If the text is too short, return it as is
    if len(text.split()) < 50:
        return text
    
    # If the letter count is 3000 or less, summarize directly
    pipe = ModelLoader.get_pipeline()
    if len(text) < 3000:
        return generate_final_summary(text, pipe)

    
    # 3. Chunking and Summarization (The Map Step)
    chunks = chunk_text(text)
    partial_summaries = []
    for i, chunk in enumerate(chunks):
        # print(f"     - Chunk {i+1}/{len(chunks)}")
        summary = summarize_chunk(chunk, pipe)
        partial_summaries.append(summary)

    # 4. Final Summary (The Reduce Step)
    combined_summaries = "\n".join(partial_summaries)
    final_output = generate_final_summary(combined_summaries, pipe)
    
    return final_output