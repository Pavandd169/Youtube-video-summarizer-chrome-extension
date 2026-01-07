from summarizer.summarize import summarize_transcript

def main():
    with open("data/sample.txt", "r") as f:
        transcript = f.read()

    summary = summarize_transcript(transcript)
    print("\nSUMMARY:\n")
    print(summary)

if __name__ == "__main__":
    main()