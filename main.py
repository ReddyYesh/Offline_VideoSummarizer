import argparse
import os

from downloader import download_audio
from transcriber import OfflineTranscriber
from summarizer import OfflineSummarizer


def main():
    parser = argparse.ArgumentParser(description="Offline YouTube Video Summarizer")
    parser.add_argument("url", help="YouTube video URL")
    parser.add_argument(
        "--output_dir",
        default="outputs",
        help="Directory to save transcript and summary",
    )
    parser.add_argument(
        "--max_sentences",
        type=int,
        default=5,
        help="Maximum number of sentences in the final summary",
    )
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)

    # 1) Download audio
    print("[1/3] Downloading audio from YouTube...")
    audio_path = download_audio(args.url)
    print(f"    Audio downloaded to: {audio_path}")

    # 2) Transcribe audio (Vosk)
    print("[2/3] Transcribing audio (offline, Vosk)...")
    transcriber = OfflineTranscriber()
    transcript = transcriber.transcribe(audio_path)

    transcript_path = os.path.join(args.output_dir, "transcript.txt")
    with open(transcript_path, "w", encoding="utf-8") as f:
        f.write(transcript)
    print(f"    Transcript saved to: {transcript_path}")

    # 3) Summarize transcript (our offline extractive summarizer)
    print("[3/3] Summarizing transcript (offline)...")
    summarizer = OfflineSummarizer(max_sentences=args.max_sentences)
    summary = summarizer.summarize(transcript)

    summary_path = os.path.join(args.output_dir, "summary.txt")
    with open(summary_path, "w", encoding="utf-8") as f:
        f.write(summary)
    print(f"    Summary saved to: {summary_path}")

    print("\n===== FINAL SUMMARY =====\n")
    print(summary)
    print("\n=========================\n")
    print("Done.")


if __name__ == "__main__":
    main()
