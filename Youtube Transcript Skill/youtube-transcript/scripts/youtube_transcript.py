"""
YouTube Transcript Downloader
Extracts transcript/subtitles from a YouTube video and saves as .txt

Dependencies: youtube-transcript-api, requests
Install:     pip install youtube-transcript-api requests --break-system-packages

Usage:
  python youtube_transcript.py <URL_or_VideoID> [language] [--no-timestamps] [--output filename.txt]
"""

import sys
import re
import json
import argparse
import requests
from youtube_transcript_api import YouTubeTranscriptApi


def extract_video_id(url_or_id: str) -> str:
    """Extract video ID from various YouTube URL formats or accept raw ID."""
    patterns = [
        r"(?:v=|/v/|youtu\.be/|/embed/|/shorts/)([a-zA-Z0-9_-]{11})",
        r"^([a-zA-Z0-9_-]{11})$",
    ]
    for pattern in patterns:
        match = re.search(pattern, url_or_id)
        if match:
            return match.group(1)
    raise ValueError(f"Cannot extract Video ID from: {url_or_id}")


def format_timestamp(seconds: float) -> str:
    """Convert seconds to HH:MM:SS or MM:SS."""
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    return f"{h:02d}:{m:02d}:{s:02d}" if h > 0 else f"{m:02d}:{s:02d}"


def fetch_video_title(video_id: str) -> str:
    """Fetch video title from YouTube oembed API."""
    try:
        url = f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={video_id}&format=json"
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        return resp.json().get("title", "")
    except Exception:
        return ""


def make_short_name(title: str, max_words: int = 4) -> str:
    """Shorten a video title to a few key words, safe for filenames."""
    if not title:
        return ""
    # Remove common noise: brackets, pipes, dashes used as separators
    title = re.sub(r"\s*[\|\-–—]\s*.*$", "", title)  # drop "| Channel Name" suffix
    title = re.sub(r"[\[\(].*?[\]\)]", "", title)     # drop [Official Video] etc.
    title = re.sub(r"[^\w\s฀-๿]", "", title)  # keep alphanum, spaces, Thai chars
    words = title.split()
    short = " ".join(words[:max_words])
    # Clean up for filesystem safety
    short = re.sub(r"\s+", " ", short).strip()
    return short if short else ""


def get_transcript(video_id: str, lang: str = None) -> list:
    """Fetch transcript from YouTube. Tries th/en by default."""
    api = YouTubeTranscriptApi()
    if lang:
        return api.fetch(video_id, languages=[lang])
    try:
        return api.fetch(video_id, languages=["th", "en"])
    except Exception:
        return api.fetch(video_id)


def save_transcript(transcript, output_path: str, include_timestamps: bool = True) -> int:
    """Save transcript to a text file. Returns line count."""
    with open(output_path, "w", encoding="utf-8") as f:
        for entry in transcript:
            if include_timestamps:
                f.write(f"[{format_timestamp(entry.start)}] {entry.text}\n")
            else:
                f.write(f"{entry.text}\n")
    return len(transcript)


def main():
    parser = argparse.ArgumentParser(description="Download YouTube transcript as .txt")
    parser.add_argument("url", help="YouTube URL or Video ID")
    parser.add_argument("lang", nargs="?", default=None, help="Language code (e.g. th, en)")
    parser.add_argument("--no-timestamps", action="store_true", help="Omit timestamps")
    parser.add_argument("--output", "-o", default=None, help="Output filename (default: transcript_<id>.txt)")
    args = parser.parse_args()

    try:
        video_id = extract_video_id(args.url)
        transcript = get_transcript(video_id, args.lang)

        if args.output:
            output_path = args.output
        else:
            title = fetch_video_title(video_id)
            short = make_short_name(title)
            output_path = f"Transcript {short}.txt" if short else f"Transcript {video_id}.txt"

        count = save_transcript(transcript, output_path, not args.no_timestamps)
        print(f"Saved: {output_path} ({count} lines)")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
