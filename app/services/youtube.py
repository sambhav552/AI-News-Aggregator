from datetime import datetime, timedelta, timezone
from typing import List, Optional
import os
import feedparser
from pydantic import BaseModel
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound
from youtube_transcript_api.proxies import WebshareProxyConfig

def get_transcript( video_id: str) -> Optional[str]:
    try:
        transcript = YouTubeTranscriptApi().fetch(video_id = video_id)
        return " ".join(snippet.text for snippet in transcript)
    except (TranscriptsDisabled, NoTranscriptFound):
        return None
    except Exception:
        return None

if __name__ == "__main__":
    print(get_transcript("E8zpgNPx8jE"))