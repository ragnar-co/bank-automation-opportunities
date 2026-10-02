# Automation Opportunity Finder — GLOSSARY

Project: `Automation Opportunity Finder`  
Document ID: `glossary`  
Template: `ddd-web-app-v2.8.0`  
Status: Draft for implementation  
Depends on: `personas`, `prd`

## Term Definitions

| Term | Definition | Owning Role |
|---|---|---|
| Task | งานหนึ่งรายการจาก CSV ที่มี `task_id`, department, task name, frequency และเวลาต่อครั้ง | Product/Analyst |
| Department | หน่วยงานเจ้าของ/ที่เกี่ยวข้องกับ task ตามค่า `department` ใน dataset | Product/Analyst |
| Weekly Run | จำนวนครั้งที่ task เกิดขึ้นต่อสัปดาห์จาก `weekly_runs` | Product/Analyst |
| Minutes per Run | นาทีที่ใช้ต่อหนึ่งครั้งของ task จาก `minutes_per_run` | Product/Analyst |
| Weekly Effort | เวลาที่ใช้กับ task ต่อสัปดาห์ คำนวณ `weekly_runs × minutes_per_run`; เป็น current effort ไม่ใช่ automation savings | Product/Analyst |
| Department Weekly Effort | ผลรวม Weekly Effort ของ task ทุกตัวใน department เดียวกัน | Product/Analyst |
| Top 3 Task | สาม task ที่มี Weekly Effort สูงสุดใน dataset ที่ persist อยู่ | Product/Analyst |
| Automation Opportunity | งานที่ถูกนำไปพิจารณาสำรวจ Automation ต่อ; คำนี้ไม่แปลว่างานนั้น automate ได้แน่นอน | Product/Analyst |
| Exploration Recommendation | ข้อเสนอจาก AI bonus เพื่อช่วยตั้งประเด็นสำรวจต่อ พร้อมเหตุผลและสิ่งที่ต้องตรวจสอบ | Product/Analyst |
| Automation Savings | เวลาที่ประหยัดได้จริงหลัง Automation; dataset ปัจจุบันไม่มีข้อมูลพอสำหรับคำนวณค่านี้ | Business owner |

## Term-to-Entity Mapping

| Term | Current Mapping | Notes |
|---|---|---|
| Task | `tasks` | confirmed by DATA_MODEL.md |
| Department | `tasks.department` | ค่า source จาก CSV |
| Weekly Run | `tasks.weekly_runs` | source field |
| Minutes per Run | `tasks.minutes_per_run` | source field |
| Weekly Effort | query expression `weekly_runs * minutes_per_run` | ไม่จำเป็นต้อง persist เป็น column |
| Exploration Recommendation | `exploration_recommendations` | confirmed by DATA_MODEL.md; supersedes the earlier placeholder name `ai_recommendations` |

## Disputed Terms

| Term | Decision |
|---|---|
| `weekly_time` vs `weekly_effort` | ใช้คำผู้ใช้ว่า “Weekly Effort” เพื่อหลีกเลี่ยงการตีความเป็น savings; identifier เชิงเทคนิคใช้ `weekly_minutes` ได้ |
| `recommendation` | ต้องเขียนเต็มในบริบทว่า “Exploration Recommendation”; ห้ามใช้เพื่อสื่อว่าเป็นคำตัดสินให้ automate ทันที |
| `savings` | ห้ามใช้แทน Weekly Effort; ใช้ได้เมื่อมีข้อมูล realized/estimated savings ที่ผ่านวิธีวัดแยกต่างหากในอนาคต |

## Glossary Change Log

| Revision | Change |
|---|---|
| Draft-1 | สร้างคำศัพท์หลักจากโจทย์, CSV schema และ PRD ของ Automation Opportunity Finder |
| Draft-2 | Reconciled Term-to-Entity Mapping against `docs/DATA_MODEL.md`: Exploration Recommendation now maps to `exploration_recommendations` (was placeholder `ai_recommendations`) |

## Enumeration Registry

ทะเบียนนี้เป็น index เท่านั้น และจงใจไม่ใส่ค่า enum จริง.

| Enum | Owner Document |
|---|---|
| `requirement_priority` | SCOPE.md |
| `adr_status` | ADR.md |
| `work_item_status` | TASKS.md |
| `pdpa_classification` | DATA_MODEL.md |
| `environment` | ARCHITECTURE.md |
| `incident_severity` | RUNBOOK.md |
| `role` | SECURITY.md |
| `application_error_code` | API_SPEC.md |
| `event_name` | TRACKING_PLAN.md |
| `deployment_strategy` | DEPLOYMENT.md |
| `confidentiality_class` | DATA_MODEL.md |

Validation Checklist
- [x] นิยามคำสำคัญของ PRD และ dataset
- [x] แยก Weekly Effort ออกจาก Automation Savings ชัดเจน
- [x] Enumeration Registry ไม่มีค่า enum จริง
- [x] mapping ที่ต้องรอเอกสารปลายทางถูกระบุว่าเป็นค่าคาดหมายและต้อง reconcile รอบสอง
