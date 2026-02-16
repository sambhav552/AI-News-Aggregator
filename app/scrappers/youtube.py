from datetime import datetime, timedelta, timezone
from typing import List, Optional
import os
import feedparser
from pydantic import BaseModel
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound
from youtube_transcript_api.proxies import WebshareProxyConfig


def get_rss_url(channel_id: str) -> str:
    return f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"

def extract_video_id(video_url: str) -> str:
    if "youtube.com/watch?v=" in video_url:
        return video_url.split("v=")[1].split("&")[0]
    if "youtube.com/shorts/" in video_url:
        return video_url.split("shorts/")[1].split("?")[0]
    if "youtu.be/" in video_url:
        return video_url.split("youtu.be/")[1].split("?")[0]
    return video_url

def get_transcript( video_id: str) -> Optional[str]:
    try:
        transcript = YouTubeTranscriptApi().fetch(video_id)
        return " ".join(snippet.text for snippet in transcript)
        
    except (TranscriptsDisabled, NoTranscriptFound):
        return None
    except Exception:
        return None

def get_latest_videos( channel_id: str, hours: int = 24) -> list[dict]:
    feed = feedparser.parse(get_rss_url(channel_id))
    if not feed.entries:
        return []
    
    cutoff_time = datetime.now(timezone.utc) - timedelta(hours=hours)
    videos = []
    
    for entry in feed.entries:
        if "/shorts/" in entry.link:
            continue
        published_time = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)
        if published_time >= cutoff_time:
            video_id = extract_video_id(entry.link)
            videos.append({
                "title":entry.title,
                "url":entry.link,
                "video_id":video_id,
                "published_at":published_time,
                "description":entry.get("summary", "")
            })
    
    return videos

def scrape_channel( channel_id: str, hours: int = 150) -> list[dict]:
    videos = get_latest_videos(channel_id, hours)
    result = []
    for video in videos:
        video["transcript"] = get_transcript(video["video_id"])
    return videos
    
    
    
if __name__ == "__main__":
    # feed = feedparser.parse(get_rss_url("UCn8ujwUInbJkBhffxqAPBVQ"))
    # print(len(feed.entries))
    videos = get_latest_videos(channel_id = "UCn8ujwUInbJkBhffxqAPBVQ", hours=4000)
    print(videos)
    
    
