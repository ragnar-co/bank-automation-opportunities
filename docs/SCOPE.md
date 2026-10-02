# Automation Opportunity Finder — SCOPE

Project: `Automation Opportunity Finder`  
Document ID: `scope`  
Template: `ddd-web-app-v2.8.0`  
Status: Draft for implementation  
Depends on: `vpd`, `personas`

## MVP Feature List

`requirement_priority` ใช้ตาม template: `P0` = Must, `P1` = Should, `P2` = Nice.

| Priority | Feature | Rationale |
|---|---|---|
| P0 | CSV ingestion จากไฟล์ตัวอย่าง | เป็น input ที่โจทย์กำหนด |
| P0 | CSV validation ก่อน persist | โจทย์กำหนดให้ตรวจสอบข้อมูล |
| P0 | Persist ข้อมูลลง SQLite3 | โจทย์กำหนด SQLite3 หรือ DuckDB; โปรเจกต์เลือก SQLite3 |
| P0 | แสดงเวลาต่อสัปดาห์ของแต่ละงาน | core output |
| P0 | แสดงเวลารวมต่อสัปดาห์แยกตามแผนก | core output |
| P0 | แสดง Top 3 งานที่ใช้เวลามากที่สุด | core output |
| P0 | Web UI สำหรับเปิดดูผล | core interaction ที่โจทย์กำหนด |
| P0 | Disclaimer ว่า current effort ไม่ใช่ automation savings | ข้อกำหนด explicit ของโจทย์ |
| P0 | Deploy ผ่าน Coolify และเปิดใช้งานได้ | submission requirement |
| P1 | AI exploration recommendations ที่ persist และแสดงบน UI | โบนัส 10 คะแนน |

## Out-of-Scope Items

| Item | Reason | Destination |
|---|---|---|
| CSV Upload UI | โจทย์ไม่ได้กำหนดว่าผู้ใช้ต้อง upload ผ่าน UI; ลดความเสี่ยงใน 120 นาที | Future enhancement |
| Automation savings estimate | ไม่มีข้อมูล automatable percentage, exception rate, implementation cost หรือ realized savings | ต้องมี discovery/data เพิ่มก่อน |
| Automation feasibility score แบบตัวเลข | ไม่มีสูตรหรือ calibration source จากโจทย์ | Future validated model |
| User/role management | ไม่ได้อยู่ใน requirement ที่ได้รับ | Future enhancement หากมี requirement |
| Parsing customer/project/team ออกจาก `task_name` | ไม่จำเป็นต่อ core outputs และเพิ่ม parsing risk | Future enhancement |
| Editable task CRUD | app นี้เป็น analysis/viewer ตามโจทย์ ไม่ใช่ task management system | Out of current release |

## Phase Roadmap

| Phase | Goal | Exit condition |
|---|---|---|
| Core | CSV → validate → SQLite3 → analytics UI | core requirements แสดงผลถูกต้องและ production เปิดได้ |
| Bonus | AI วิเคราะห์ข้อมูลจาก DB และสร้าง exploration proposal | recommendation ถูก persist และเปิดดูใน UI ได้ |
| Post-exam | hardening/UX/authorization/advanced analytics | ทำเมื่อมี requirement และ calibration data จริง |

## External Dependencies

| Dependency | Owner | Needed for | Status |
|---|---|---|---|
| `bank_automation_opportunities.csv` | Exam package | Core | Available |
| Company Git repository | Developer | Submission | Access required |
| Coolify | Developer/Platform | Production deploy | Access required |
| Claude Code/Codex | Developer | Implementation workflow | Available per brief |
| Company AI endpoint + quota | Platform owner | Bonus only | Endpoint/quota details to confirm |

Validation Checklist
- [x] มี MVP, out-of-scope, roadmap และ external dependencies
- [x] ทุก out-of-scope มีเหตุผล
- [x] แยก core 100 คะแนนออกจาก bonus 10 คะแนน
- [x] ไม่สร้าง savings/feasibility score ที่ข้อมูลไม่รองรับ
- [x] ไม่มี CSV Upload UI ใน current scope
