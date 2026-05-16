# Useful AI Skills

รวม skills สำหรับ Claude Code และ Claude Cowork

## Skills

| Skill | Description |
|-------|-------------|
| [SET-API Skill](./SET-API%20Skill/) | ดึงข้อมูลจากตลาดหลักทรัพย์แห่งประเทศไทย (SET) — ข่าว, งบการเงิน, ราคาหุ้น, NVDR, วอร์แรนต์, รายงานประจำปี |

## Installation

### Claude Cowork
อัปโหลดไฟล์ `.skill` จาก folder ของ skill นั้นๆ เข้า session ได้เลย

### Claude Code (CLI) — ระดับ project
```bash
mkdir -p .claude/skills
cp -r "SET-API Skill/set-api" .claude/skills/
```

### Claude Code (CLI) — ระดับ global
```bash
mkdir -p ~/.claude/skills
cp -r "SET-API Skill/set-api" ~/.claude/skills/
```
