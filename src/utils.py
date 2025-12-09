from urllib.parse import urlparse

def is_valid_youtube_url(url: str) -> bool:
    """
    Basic check to ensure the URL looks like a YouTube link.
    """
    try:
        parsed = urlparse(url)
        host = parsed.netloc.lower()
        return "youtube.com" in host or "youtu.be" in host
    except Exception:
        return False
