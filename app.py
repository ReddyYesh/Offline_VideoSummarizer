import os
import streamlit as st

from src.downloader import download_audio
from src.transcriber import OfflineTranscriber
from src.summarizer import OfflineSummarizer


def main():
    st.title("Offline YouTube Video Summarizer")

    st.write(
        "Paste a YouTube URL below. "
        
    )

    url = st.text_input("YouTube URL")
    max_sentences = st.slider(
        "Maximum number of sentences in summary",
        min_value=3,
        max_value=10,
        value=5,
    )

    if st.button("Summarize") and url:
        with st.spinner("Processing... this may take a bit for longer videos."):
            try:
                output_dir = "outputs"
                os.makedirs(output_dir, exist_ok=True)

                # 1) Download audio
                st.write("### Step 1: Downloading audio")
                audio_path = download_audio(url)
                st.write(f"Audio downloaded to: `{audio_path}`")

                # 2) Transcribe with Vosk
                st.write("### Step 2: Transcribing audio ")
                transcriber = OfflineTranscriber()
                transcript = transcriber.transcribe(audio_path)

                transcript_path = os.path.join(output_dir, "transcript_streamlit.txt")
                with open(transcript_path, "w", encoding="utf-8") as f:
                    f.write(transcript)
                st.write(f"Transcript saved to: `{transcript_path}`")

                # 3) Summarize transcript
                st.write("### Step 3: Summarizing transcript")
                summarizer = OfflineSummarizer(max_sentences=max_sentences)
                summary = summarizer.summarize(transcript)

                summary_path = os.path.join(output_dir, "summary_streamlit.txt")
                with open(summary_path, "w", encoding="utf-8") as f:
                    f.write(summary)
                st.write(f"Summary saved to: `{summary_path}`")

                st.success("Done!")

                st.subheader("Summary")
                st.write(summary)

                st.subheader("Transcript (first 1000 characters)")
                st.text_area(
                    "Transcript preview",
                    transcript[:1000],
                    height=200,
                )

            except Exception as e:
                st.error(f"Something went wrong: {e}")

    st.caption("All processing is done locally using offline models (Vosk STT + custom summarizer).")


if __name__ == "__main__":
    main()
