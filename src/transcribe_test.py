import argparse
from transcriber import OfflineTranscriber


def main():
    print(">>> Starting transcribe_test.py")

    parser = argparse.ArgumentParser(description="Test offline STT with Vosk")
    parser.add_argument("audio_path", help="Path to audio file (e.g. downloads\\file.webm)")
    args = parser.parse_args()

    print(f">>> Audio path argument: {args.audio_path}")

    stt = OfflineTranscriber()
    print(">>> OfflineTranscriber created")

    transcript = stt.transcribe(args.audio_path)
    print(">>> Transcription finished!")

    print("\n===== TRANSCRIPT (first 500 chars) =====\n")
    print(transcript[:500])
    print("\n========================================\n")


if __name__ == "__main__":
    main()
