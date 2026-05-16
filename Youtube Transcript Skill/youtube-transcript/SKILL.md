---
name: youtube-transcript
description: |
  Extract transcripts and subtitles from YouTube videos and save as text files.
  Use when the user asks to: get a YouTube transcript, download YouTube subtitles,
  extract text from a YouTube video, ดึง transcript จาก YouTube, ดาวน์โหลดคำบรรยาย YouTube,
  or any request involving reading/saving captions from a YouTube URL or video ID.
  Supports multiple languages, optional timestamps, and custom output filenames.
---

# Youtube Transcript

Extract transcripts from YouTube videos using the bundled `scripts/youtube_transcript.py`.

## Setup

Install the dependency before first use:

```bash
pip install youtube-transcript-api requests --break-system-packages
```

## Workflow

1. Identify the YouTube URL or video ID from the user's request.
2. Run the script:

```bash
python scripts/youtube_transcript.py <URL_or_ID> [lang] [--no-timestamps] [--output file.txt]
```

**Arguments:**

- `URL_or_ID` — Full YouTube URL or 11-char video ID. Supports youtube.com, youtu.be, shorts, and embed URLs.
- `lang` (optional) — Language code (`th`, `en`, `ja`, etc.). Defaults to Thai then English.
- `--no-timestamps` — Omit `[MM:SS]` prefixes from each line.
- `--output` / `-o` — Custom output filename. Defaults to `Transcript <short video title>.txt` (auto-fetched from YouTube).

3. Provide the resulting `.txt` file to the user.

## Error Handling

- If the video has no transcript available, inform the user — some videos have captions disabled.
- If a requested language is unavailable, retry without the language flag to get whatever is available, and let the user know which language was returned.
