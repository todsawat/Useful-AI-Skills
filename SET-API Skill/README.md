# SET API

เครื่องมือดึงข้อมูลจากตลาดหลักทรัพย์แห่งประเทศไทย (set.or.th) โดยไม่ต้องใช้ browser

## Features

- ค้นหาข่าวหุ้น (news search)
- ดูกำไร/EPS ด่วนจาก F45 (quick earnings view)
- ดาวน์โหลดงบการเงิน (financial statements ZIP)
- ข้อมูลหุ้น — ราคา, ผู้ถือหุ้น, corporate action, profile
- ข้อมูลวอร์แรนต์
- รายงานประจำปี / 56-1 One Report / ESG Report

## Installation

### Claude Cowork (แนะนำ)

อัปโหลดไฟล์ `set-api.skill` เข้า session ได้เลย — Claude จะโหลด skill โดยอัตโนมัติ

### Claude Code (CLI) — ระดับ project

```bash
mkdir -p .claude/skills
cp -r set-api .claude/skills/
```

จากนั้น Claude Code จะสามารถใช้ skill นี้ได้ทันทีใน project นั้น

### Claude Code (CLI) — ระดับ global (ใช้ได้ทุก project)

```bash
mkdir -p ~/.claude/skills
cp -r set-api ~/.claude/skills/
```

---

## Requirements

- Python 3.7+
- Node.js (สำหรับ eval SET's `__NUXT__` SSR data)

## Usage

```bash
cd set-financial-statements/scripts

# ค้นข่าวหุ้น
python3 download_fs.py news --symbol BH
python3 download_fs.py news --from-date 14/05/2026 --to-date 14/05/2026

# ดูกำไร/EPS ด่วน (F45)
python3 download_fs.py quick --symbol BH --quarters 4
python3 download_fs.py quick --from-date 14/05/2026 --to-date 14/05/2026

# ดาวน์โหลดงบการเงิน
python3 download_fs.py financial --symbol BH --quarters 8 --out ./output
python3 download_fs.py financial --from-date 14/05/2026 --to-date 14/05/2026 --out ./output

# ข้อมูลหุ้น
python3 download_fs.py stock --symbol BH
python3 download_fs.py stock --symbol BH --sections price,shareholders

# วอร์แรนต์
python3 download_fs.py warrant --symbol ORI

# รายงานประจำปี / 56-1
python3 download_fs.py report --symbol BH --type one --out ./output
```

## Modes

| Mode | Description |
|------|-------------|
| `news` | ค้นหาข่าวบริษัทจาก SET |
| `quick` | ดู F45 สรุปผลการดำเนินงาน (กำไร/EPS) โดยไม่ต้องโหลดไฟล์ |
| `financial` | ดาวน์โหลดงบการเงิน (ZIP: XLSX + DOCX) |
| `stock` | ราคาหุ้น, ประวัติการซื้อขาย, ผู้ถือหุ้น, corporate action, profile |
| `warrant` | ราคาวอร์แรนต์, ราคาใช้สิทธิ, วันหมดอายุ |
| `report` | รายงานประจำปี, 56-1 One Report, ESG Report |

## Project Structure

```
set-api/
├── SKILL.md              # คู่มือการใช้งาน skill
├── references/
│   └── set-api.md        # เอกสาร SET API endpoints
└── scripts/
    └── download_fs.py    # script หลัก
```

## Notes

- Date format ต้องเป็น `DD/MM/YYYY` เท่านั้น
- ใช้ Incapsula session cookies อัตโนมัติ (visit SET ก่อน แล้วดึง cookies)
- งบการเงิน ZIP ประกอบด้วย: `FINANCIAL_STATEMENTS.XLSX`, `AUDITOR_REPORT.DOCX`, `NOTES.DOCX`
