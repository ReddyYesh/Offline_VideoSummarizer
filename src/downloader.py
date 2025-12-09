import os
import yt_dlp


def download_audio(youtube_url: str, output_dir: str = "downloads") -> str:
    os.makedirs(output_dir, exist_ok=True)

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": os.path.join(output_dir, "%(id)s.%(ext)s"),
        "quiet": False,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(youtube_url, download=True)
        video_id = info.get("id")
        filename = ydl.prepare_filename(info)

        # This file will be something like: downloads/<id>.webm OR .m4a
        return filename
