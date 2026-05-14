---
name: set-api
description: >
  Search news, download financial statements (งบการเงิน), and view stock information from
  the Stock Exchange of Thailand (SET) website (set.or.th). No browser required. Supports:
  (1) searching company news for individual stocks or all stocks by date,
  (2) downloading financial statements for individual stocks (multiple quarters) or all stocks
  on a specific date, (3) quick F45 earnings view, (4) stock information (price, historical
  trading, shareholders, corporate actions, company profile), (5) warrant information,
  (6) annual reports / 56-1 One Report / ESG reports. Use when: "download financial
  statements from SET", "get งบการเงิน", "download SET filing", "get BH/PTT/ADVANC financial
  statements", "โหลดงบการเงินจาก SET", "ดาวน์โหลดงบการเงิน", "งบการเงินจากตลาดหลักทรัพย์",
  "SET financial data", "quarterly financials from SET", "ข่าวหุ้น SET", "ข่าวหุ้น BH",
  "search SET news", "SET company news", "หาข่าวจาก SET", "ข่าวตลาดหลักทรัพย์",
  "งบทุกตัววันนี้", "all financial statements today", "ดูงบด่วน", "F45", "สรุปผลการดำเนินงาน",
  "quick earnings", "ดูกำไรขาดทุน", "EPS ล่าสุด", "ราคาหุ้น", "stock price", "ข้อมูลหุ้น",
  "stock info", "ผู้ถือหุ้นใหญ่", "major shareholders", "สิทธิประโยชน์", "XD", "corporate action",
  "historical trading", "ประวัติการซื้อขาย", "company profile", "ข้อมูลบริษัท",
  "PE ratio", "PB ratio", "market cap", "dividend yield",
  "warrant", "ใบสำคัญแสดงสิทธิ", "วอร์แรนต์", "exercise price", "ราคาใช้สิทธิ",
  "รายงานประจำปี", "annual report", "56-1", "One Report", "ESG report",
  "กรรมการบริษัท", "board of directors",
  or any request to search Thai stock news, view stock data, check warrants, download
  annual reports, or retrieve listed company filings from set.or.th.
---

# SET News, Financial Statements & Stock Info

Search company news, download financial statements, and view stock information from the Stock Exchange of Thailand (set.or.th). No browser required.

## Requirements

- Python 3.7+
- Node.js (for evaluating SET's __NUXT__ SSR data)

## Modes

The script `scripts/download_fs.py` has six modes: `news`, `quick`, `financial`, `stock`, `warrant`, and `report`.

### Mode: news

Search and display SET company news.

```bash
# News for a single stock
python3 scripts/download_fs.py news --symbol BH

# All company news on a specific date
python3 scripts/download_fs.py news --from-date 14/05/2026 --to-date 14/05/2026

# Filter headlines with regex
python3 scripts/download_fs.py news --from-date 01/05/2026 --to-date 14/05/2026 --filter "งบการเงิน"

# JSON output
python3 scripts/download_fs.py news --symbol ADVANC --format json

# With keyword search
python3 scripts/download_fs.py news --keyword "เงินปันผล" --from-date 01/01/2026 --to-date 14/05/2026
```

**news arguments:** `--symbol`, `--from-date DD/MM/YYYY`, `--to-date DD/MM/YYYY`, `--keyword`, `--filter` (regex on headline), `--limit` (default 200), `--format` (table|json), `--show-id`

### Mode: quick

Quick view of F45 earnings summaries (สรุปผลการดำเนินงาน) — shows profit and EPS inline without downloading files. The content is returned as-is from SET for Claude to read and interpret directly.

```bash
# Quick view BH earnings (last 4 quarters)
python3 scripts/download_fs.py quick --symbol BH --quarters 4

# Quick view all F45 filed on a specific date
python3 scripts/download_fs.py quick --from-date 14/05/2026 --to-date 14/05/2026

# JSON output (for programmatic use)
python3 scripts/download_fs.py quick --symbol BH --quarters 2 --format json
```

**quick arguments:** `--symbol`, `--from-date DD/MM/YYYY`, `--to-date DD/MM/YYYY`, `--quarters` (default 4), `--limit`, `--format` (text|json)

**Tip:** Use `quick` when the user wants a fast overview of earnings (กำไร/ขาดทุน, EPS). The F45 content is plain text — do NOT try to regex-parse it; read it directly as AI and extract the relevant numbers.

### Mode: financial

Download financial statement files (ZIP containing XLSX + DOCX, or PDF).

```bash
# Single stock, 8 quarters
python3 scripts/download_fs.py financial --symbol BH --quarters 8 --out ./output

# All stocks that filed on a specific date
python3 scripts/download_fs.py financial --from-date 14/05/2026 --to-date 14/05/2026 --out ./output

# List available downloads without downloading
python3 scripts/download_fs.py financial --symbol PTT --quarters 4 --list-only

# All stocks on a date range, limit total downloads
python3 scripts/download_fs.py financial --from-date 01/05/2026 --to-date 14/05/2026 --limit 20 --out ./output
```

**financial arguments:** `--symbol`, `--from-date DD/MM/YYYY`, `--to-date DD/MM/YYYY`, `--quarters` (per symbol, default 8), `--limit` (max total), `--out` (output dir), `--list-only`

### Mode: stock

View stock information — price quotes, historical trading data, shareholders, corporate actions, and company profile. Output is raw JSON for AI to interpret.

```bash
# All stock info sections
python3 scripts/download_fs.py stock --symbol BH

# Specific sections only
python3 scripts/download_fs.py stock --symbol BH --sections price,shareholders

# Historical trading with date range
python3 scripts/download_fs.py stock --symbol BH --sections historical --from-date 01/05/2026 --to-date 14/05/2026

# Company profile and financial ratios
python3 scripts/download_fs.py stock --symbol PTT --sections profile
```

**stock arguments:** `--symbol` (required), `--sections` (comma-separated, default: all), `--from-date DD/MM/YYYY`, `--to-date DD/MM/YYYY` (for historical trading only)

**Available sections:**

| Section | Description | SET API endpoints used |
|---------|-------------|----------------------|
| `price` | Realtime price, PE/PB/yield, 52w range, price performance | `/info`, `/highlight-data`, `/price-performance` |
| `historical` | Daily OHLCV history | `/historical-trading` |
| `rights` | XD/XR/XM corporate actions | `/corporate-action` |
| `shareholders` | Major shareholders list | `/shareholder` |
| `profile` | Company name, sector, key financial ratios | `/profile`, `/key-financial-data` |

**Tip:** Output is raw JSON — do NOT try to parse or format it in the script; read it directly as AI and extract the relevant information for the user.

### Mode: warrant

Check warrant information for a stock — lists all related warrants with realtime price and detailed terms (exercise price, ratio, maturity date).

```bash
# Check warrants for a stock
python3 scripts/download_fs.py warrant --symbol ORI

# Stock without warrants returns empty list
python3 scripts/download_fs.py warrant --symbol BH
```

**warrant arguments:** `--symbol` (required, parent stock symbol)

**Output includes:** For each warrant: realtime quote (last price, change, volume) and profile (exercise price, exercise ratio, maturity date, underlying symbol, listed/converted shares).

### Mode: report

List or download annual reports (56-1 One Report), ESG reports, and board of directors info.

```bash
# List all available reports
python3 scripts/download_fs.py report --symbol BH

# List only 56-1 One Report
python3 scripts/download_fs.py report --symbol BH --type one

# Download latest 56-1 One Report
python3 scripts/download_fs.py report --symbol BH --type one --out ./output

# Download a specific year
python3 scripts/download_fs.py report --symbol BH --type one --year 2024 --out ./output

# Download latest ESG report
python3 scripts/download_fs.py report --symbol PTT --type esg --out ./output

# Download multiple report types, 3 years each
python3 scripts/download_fs.py report --symbol BH --type one,esg --limit 3 --out ./output
```

**report arguments:** `--symbol` (required), `--type` (comma-separated: one/annual/form56/esg, default: all), `--year`, `--limit`, `--out` (output dir, omit to list only), `--list-only`

**Available report types:**

| Type | Description |
|------|-------------|
| `one` | 56-1 One Report (แบบ 56-1 One Report) — most common modern format |
| `annual` | Annual Report (รายงานประจำปี) — older format, many companies now use `one` |
| `form56` | Form 56-1 (แบบ 56-1) — older format |
| `esg` | ESG Report |

**Note:** Board of directors is automatically included when listing all report types.

## Important Notes

- Date format MUST be `DD/MM/YYYY` — other formats return HTTP 400.
- Without `--from-date`, single-stock mode defaults to last 3 years; all-stocks mode defaults to today.
- Corrected filings (headline contains "แก้ไข") are automatically deduplicated — only the latest version is kept.
- Each ZIP typically contains: `FINANCIAL_STATEMENTS.XLSX`, `AUDITOR_REPORT.DOCX`, `NOTES.DOCX`.
- For technical details on SET's API, see [references/set-api.md](references/set-api.md).
