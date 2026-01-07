from summarizer.chunker import chunk_text
from summarizer.preprocess import normalize_transcript

def main():
    with open("data/sample.txt", "r") as f:
        transcript = f.read()

    transcript = normalize_transcript(transcript)
    chunks = chunk_text(transcript)
    print(type(chunks))
    print('Number of chunks: ',len(chunks))
    print('Lengths of each chunk:')
    for i, chunk in enumerate(chunks):
        print(len(chunk.split(' ')))

if __name__ == "__main__":
    main()