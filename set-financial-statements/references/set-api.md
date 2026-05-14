# SET Website Technical Reference

## Architecture

SET website (set.or.th) uses Nuxt.js with server-side rendering. Key details:

- `window.__NUXT__` contains serialized state as a self-executing JS function (not plain JSON)
- Must use Node.js `eval()` to parse it — `JSON.parse()` will not work
- News list data is loaded client-side only (`news.news = null` in SSR)
- But `newsDetails` IS available in SSR when visiting individual news detail pages

## Bot Protection (Incapsula/Imperva)

Both `set.or.th` and `weblink.set.or.th` use Incapsula bot protection.

- Must visit the domain first to obtain session cookies before API/file requests
- Cookies: `incap_ses_*`, `nlbi_*`, `visid_incap_*`, `charlot`
- Without cookies: API returns 403, file downloads return HTML challenge page

## News Search API

```
GET /api/set/news/search
```

**Parameters:**
| Param | Type | Description |
|-------|------|-------------|
| symbol | string | Stock symbol (e.g. BH, PTT) |
| sourceId | string | "company" for listed company news |
| securityType | string | "S" for stocks |
| fromDate | string | Start date in DD/MM/YYYY format |
| toDate | string | End date in DD/MM/YYYY format |
| perPage | int | Results per page |
| page | int | Page number |
| keyword | string | Search keyword |
| lang | string | "th" or "en" |

**Important:** Date format MUST be `DD/MM/YYYY`. Using `YYYY-MM-DD` returns HTTP 400.

**Required headers:**
- `Referer: https://www.set.or.th/th/market/news-and-alert/news`
- Valid Incapsula session cookies

**Response:**
```json
{
  "totalCount": 80,
  "newsInfoList": [
    {
      "id": "17768977980741",
      "datetime": "2026-04-23T07:41:00+07:00",
      "symbol": "BH",
      "source": "BH",
      "headline": "งบการเงิน ไตรมาสที่ 1/2569 (สอบทานแล้ว)",
      "url": "https://www.set.or.th/th/market/news-and-alert/newsdetails?id=..."
    }
  ]
}
```

## News Detail → Download URL

Visit the newsdetails page as HTML, extract `window.__NUXT__`, eval with Node.js:

```
state.news.newsDetails.downloadUrl
→ "https://weblink.set.or.th/dat/news/YYYYMM/FILENAME.zip"
```

## ZIP File Contents

Each financial statement ZIP typically contains 3 files:
- `FINANCIAL_STATEMENTS.XLSX` (or `.XLS`) — the actual financial data
- `AUDITOR_REPORT.DOCX` (or `.DOC`) — auditor's report
- `NOTES.DOCX` (or `.DOC`) — notes to financial statements

## Stock Information APIs

All stock APIs require Incapsula cookies (visit SET first) and standard API headers.

### Price & Quote
- `GET /api/set/stock/{symbol}/info` — Realtime: last, open, high, low, volume, change%, bids/offers, marketCap, PE, PB, dividendYield, 52w high/low
- `GET /api/set/stock/{symbol}/highlight-data` — PE, PB, dividendYield, beta, marketCap, turnoverRatio, freeFloat
- `GET /api/set/stock/{symbol}/price-performance` — % change over 5d, 1m, 3m, 6m, YTD, 1y

### Historical Trading
- `GET /api/set/stock/{symbol}/historical-trading` — Array of daily OHLCV records
  - Optional params: `fromDate=DD/MM/YYYY`, `toDate=DD/MM/YYYY`
  - Each record: date, open, high, low, close, volume, value, PE, PBV, dividendYield, marketCap

### Rights & Benefits
- `GET /api/set/stock/{symbol}/corporate-action` — XD, XR, XM records with dates, ratios, amounts

### Major Shareholders
- `GET /api/set/stock/{symbol}/shareholder` — bookCloseDate, totalShareholder, majorShareholders array (name, numberOfShare, percentOfShare)

### Company Profile
- `GET /api/set/stock/{symbol}/profile` — Company name (TH/EN), market, industry, sector, establishment date, URL
- `GET /api/set/stock/{symbol}/key-financial-data` — Financial ratios (ROA, ROE, DE ratio, etc.)

### NVDR
- `GET /api/set/stock/{symbol}/nvdr-holder` — NVDR holding details

### Warrants
- `GET /api/set/stock/{symbol}/related-product/W` — List related warrants for a stock (returns relatedProducts array with realtime quote data: last, change, exercisePrice, exerciseRatio, maturityDate)
- `GET /api/set/stock/{warrant-symbol}/profile` — Warrant profile details (e.g. `/api/set/stock/ORI-W2/profile`). Returns: exercisePrice, exerciseRatio, maturityDate, underlying, listedShare, convertedShare, status, etc.
- Note: `/api/set/stock/{warrant-symbol}/info` returns 404. Use `/profile` instead.

### Company Reports & Documents
- `GET /api/set/company/{symbol}/report/one` — 56-1 One Report (แบบ 56-1 One Report) — array of {symbol, receiveDate, year, url, remark}. URL points to ZIP on weblink.set.or.th.
- `GET /api/set/company/{symbol}/report/annual` — Annual Report (รายงานประจำปี)
- `GET /api/set/company/{symbol}/report/form56` — Form 56-1 (แบบ 56-1)
- `GET /api/set/company/{symbol}/report/esg` — ESG Report
- `GET /api/set/company/{symbol}/board-of-director` — Board of directors list (name, positions[])
- `GET /api/set/company/{symbol}/profile` — Company profile (name, market, sector, businessType, logoUrl, website, address, phone, etc.)

## Other Endpoints (limited utility)

- `/api/set/stock/{symbol}/financialstatement` — returns ONLY the latest quarter
- `/api/set/stock/{symbol}/financialstatement/latest-full-financialstatement` — same, latest only
- Financial statement page NUXT state `lastestFinancial.downloadUrl` — only 1 URL

These endpoints cannot retrieve historical data. Use the News Search API approach instead.
