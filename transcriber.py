import os
import wave
import subprocess
from vosk import Model, KaldiRecognizer



MODEL_PATH = os.path.join("models", "vosk-model-small-en-us-0.15")


FFMPEG_EXE = r"C:\ffmpeg\bin\ffmpeg.exe"


def convert_to_wav(input_path: str, output_path: str, sample_rate: int = 16000) -> None:
    
    cmd = [
        FFMPEG_EXE,
        "-y",           
        "-i", input_path,
        "-ac", "1",     # mono
        "-ar", str(sample_rate),  # sample rate
        "-vn",
        output_path,
    ]
    subprocess.run(cmd, check=True)


class OfflineTranscriber:
    def __init__(self, model_dir: str = MODEL_PATH, sample_rate: int = 16000):
        """
        Offline STT using Vosk model.
        """
        if not os.path.isdir(model_dir):
            raise RuntimeError(f"Vosk model directory not found: {model_dir}")

        print(f"[STT] Loading Vosk model from: {model_dir}")
        self.model = Model(model_dir)
        self.sample_rate = sample_rate

    def transcribe(self, audio_path: str) -> str:
        
        print(f"[STT] Converting audio to WAV: {audio_path}")
        tmp_wav = "temp_stt.wav"
        convert_to_wav(audio_path, tmp_wav, sample_rate=self.sample_rate)

        print(f"[STT] Starting transcription on: {tmp_wav}")
        wf = wave.open(tmp_wav, "rb")

        if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getframerate() != self.sample_rate:
            wf.close()
            os.remove(tmp_wav)
            raise RuntimeError("WAV file has wrong format after conversion.")

        rec = KaldiRecognizer(self.model, self.sample_rate)

        text_chunks = []
        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break
            if rec.AcceptWaveform(data):
                res = rec.Result()
                # Result is like: {"text": "some words"}
                text_part = res.split('"text" : "')[-1].rstrip('"}\n ')
                text_chunks.append(text_part)

        # Final partial result
        final_res = rec.FinalResult()
        final_text = final_res.split('"text" : "')[-1].rstrip('"}\n ')
        text_chunks.append(final_text)

        wf.close()
        os.remove(tmp_wav)

        transcript = " ".join(chunk.strip() for chunk in text_chunks if chunk.strip())
        print(f"[STT] Transcription complete. Length (chars): {len(transcript)}")

        return transcript

