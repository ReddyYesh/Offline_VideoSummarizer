# Offline YouTube Video Summarizer

This project is an end-to-end offline system that takes a YouTube video URL, downloads the audio, performs offline speech-to-text transcription, and generates a concise summary of the content. All AI components (STT + summarizer) run fully offline, satisfying the assignment’s strict no-cloud requirement.

The application includes both a CLI and a Streamlit web interface.

## Project Overview

The Offline YouTube Summarizer enables users to extract and summarize information from YouTube videos without relying on cloud services. Given a YouTube URL, the system:

1. Downloads the audio using `yt-dlp`.
2. Converts audio to WAV using FFmpeg.
3. Transcribes speech locally using the Vosk offline speech recognition model.
4. Summarizes the transcript using a custom extractive summarization model.
5. Displays (and saves) the final summary.

The entire pipeline works without internet access, except during the initial model download.

## Setup and Installation Instructions

### Prerequisites

* Python 3.10+
* FFmpeg installed and added to PATH
* Git

### Step-by-Step Setup

#### 1. Clone the Repository

```bash
git clone <your_private_repo_url>
cd offline-youtube-summarizer
```

#### 2. Create & Activate Virtual Environment

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

#### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 4. Install the Offline Vosk Model

Download:
**vosk-model-small-en-us-0.15**
from: [https://alphacephei.com/vosk/models](https://alphacephei.com/vosk/models)

Place it here:

```
offline-youtube-summarizer/models/vosk-model-small-en-us-0.15/
```

Folder should look like:

```
models/
    vosk-model-small-en-us-0.15/
        am/
        rescore/
        graph/
        ivector/
```

#### 5. Verify FFmpeg Installation

```bash
ffmpeg -version
```

## Design Choices and Justification

### Offline Speech-to-Text (Vosk)

The assignment required a fully offline STT solution. Whisper was initially considered but posed issues on Windows due to GPU/DLL dependencies and heavy model sizes. Therefore, Vosk was chosen because:

* Fully offline
* Lightweight (~40MB)
* Fast CPU inference
* No GPU required
* Cross-platform stability

**Trade-off:** Slightly lower accuracy than Whisper, but ideal given offline requirements.

### Offline Summarization Model (Custom Extractive)

Transformer-based summarizers require large downloads and heavy computation. To meet offline constraints, a custom extractive summarizer was implemented.

* Splits text into sentences (or word chunks when punctuation is missing)
* Computes word frequency scores
* Selects top-N most important sentences
* Fast and deterministic

**Trade-off:** Less natural than abstractive models, but efficient and fully offline.

## Usage

### CLI Usage

```bash
python src/main.py "<YouTube_URL>"
```

Example:

```bash
python src/main.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```

Output files:

```
outputs/transcript.txt
outputs/summary.txt
```

### Streamlit Web App

Start the app:

```bash
streamlit run app.py
```

Open:

```
http://localhost:8501
```

Paste a YouTube URL → Click **Summarize**.

## Challenges Faced

### Whisper / PyTorch DLL Issues

Whisper required GPU and Windows DLL dependencies, causing import failures. Resolved by switching to Vosk.

### Lack of Punctuation in Vosk Transcripts

Vosk outputs long text without sentence markers, breaking sentence-based summarization.

**Solution:** Implemented chunk-based splitting and frequency scoring.

### FFmpeg Not Detected Initially

yt-dlp could not post-process audio until FFmpeg was added to PATH.

### Large Directories Should Not Be Committed

`models/`, `downloads/`, and `outputs/` were excluded using `.gitignore`.

## Demonstration

A short recording should show:

* Running `streamlit run app.py`
* Pasting a YouTube URL
* Audio download
* Offline transcription
* Summary output

## Project Structure

```
offline-youtube-summarizer/
│   app.py
│   requirements.txt
│   .gitignore
│
├── src/
│   ├── downloader.py
│   ├── transcriber.py
│   ├── summarizer.py
│   ├── main.py
│
├── models/
│   └── vosk-model-small-en-us-0.15/
│
├── downloads/
├── outputs/
```
