# Youtube Transcript Skill

ดึง transcript และคำบรรยาย (subtitle) จาก YouTube วิดีโอ บันทึกเป็นไฟล์ข้อความ รองรับหลายภาษาและ timestamp

## Requirements

```bash
pip install youtube-transcript-api requests
```

## Installation

### Claude Cowork
อัปโหลดไฟล์ `youtube-transcript.skill` เข้า session ได้เลย

### Claude Code (CLI) — ระดับ project
```bash
mkdir -p .claude/skills
cp -r youtube-transcript .claude/skills/
```

### Claude Code (CLI) — ระดับ global
```bash
mkdir -p ~/.claude/skills
cp -r youtube-transcript ~/.claude/skills/
```

## Usage

```bash
# URL เต็ม (ดึง transcript ภาษา default)
python3 youtube-transcript/scripts/youtube_transcript.py https://www.youtube.com/watch?v=VIDEO_ID

# ระบุภาษา
python3 youtube-transcript/scripts/youtube_transcript.py https://youtu.be/VIDEO_ID th

# ไม่มี timestamp
python3 youtube-transcript/scripts/youtube_transcript.py VIDEO_ID en --no-timestamps

# กำหนดชื่อ output file
python3 youtube-transcript/scripts/youtube_transcript.py VIDEO_ID --output my_transcript.txt
```

## Arguments

| Argument | Description |
|----------|-------------|
| `URL_or_ID` | YouTube URL (youtube.com, youtu.be, shorts, embed) หรือ video ID 11 ตัวอักษร |
| `lang` | ภาษา เช่น `th`, `en`, `ja` (optional — default: ไทย → อังกฤษ) |
| `--no-timestamps` | ไม่แสดง `[MM:SS]` นำหน้าแต่ละบรรทัด |
| `--output` / `-o` | ชื่อไฟล์ output (default: `Transcript <ชื่อวิดีโอ>.txt`) |

## Notes

- วิดีโอบางตัวปิด caption ไว้ — skill จะแจ้งให้ทราบ
- ถ้าไม่มีภาษาที่ขอ จะดึงภาษาที่มีแล้วแจ้งให้ทราบ
