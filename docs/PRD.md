# Automation Opportunity Finder — PRD

Project: `Automation Opportunity Finder`  
Document ID: `prd`  
Template: `ddd-web-app-v2.8.0`  
Status: Draft for implementation  
Depends on: `constraints`, `personas`, `vpd`, `scope`

## Problem Statement

หลายแผนกมีงานซ้ำทุกสัปดาห์ แต่ฝ่ายบริหารยังไม่มีข้อมูลเปรียบเทียบที่ช่วยจัดลำดับว่างานใดควรถูกสำรวจ Automation ก่อน. Dataset ตัวอย่างมี task-level frequency และเวลาต่อครั้ง แต่ยังต้องถูก validate, persist, คำนวณ และสรุปให้เปิดดูผ่านหน้าจอได้. ระบบต้องสื่อให้ชัดว่า current weekly effort เป็นเพียง prioritization signal ไม่ใช่ expected automation savings.

## Goals and Success Metrics

| Goal | Baseline | Target | Measurement |
|---|---|---|---|
| G-01 ทำให้ task-level weekly effort เปิดดูผ่าน UI ได้ | CSV ดิบ | ทุก row ที่ผ่าน validation แสดง weekly effort ที่คำนวณจากสูตรเดียวกัน | เทียบค่าบน UI/DB กับ `weekly_runs * minutes_per_run` |
| G-02 ทำให้เห็น effort รวมระดับแผนก | ไม่มี summary UI | แสดง total weekly effort สำหรับทุก department ในข้อมูลที่ import | aggregate จาก DB แล้ว reconcile กับ source dataset |
| G-03 ทำให้หา 3 งานที่ใช้เวลามากที่สุดได้ทันที | ต้อง sort/คำนวณเอง | UI แสดง Top 3 ตาม `weekly_minutes DESC` | test query กับ dataset |
| G-04 ป้องกันการตีความ current effort เป็น savings | ไม่มี product UI | หน้าผลลัพธ์มี disclaimer ที่มองเห็นได้ | UI acceptance test |
| G-05 ส่งระบบที่เปิดใช้งานได้ | ยังไม่มี deployed app | production URL จาก Coolify เปิดและแสดงผล core ได้ | smoke test production |

Dataset baseline ที่ยืนยันจากไฟล์ตัวอย่าง: 12,419 rows, 8 departments. ตัวเลขนี้เป็นข้อมูลจากไฟล์ที่ได้รับ ไม่ใช่ค่ามาตรฐานของ template.

## User Stories

- US-001 — ในฐานะ `P-01 Automation Analyst` ฉันต้องการเห็น weekly effort ของแต่ละ task เพื่อเปรียบเทียบ candidate จากสูตรเดียวกัน.
- US-002 — ในฐานะ `P-01 Automation Analyst` ฉันต้องการเห็น total weekly effort แยกตาม department เพื่อรู้ว่า effort กระจุกตัวที่ใด.
- US-003 — ในฐานะ `P-01 Automation Analyst` ฉันต้องการเห็น Top 3 tasks ตาม weekly effort เพื่อเลือกหัวข้อสำหรับสำรวจต่ออย่างรวดเร็ว.
- US-004 — ในฐานะ `P-02 Management Reviewer` ฉันต้องการเห็น disclaimer ชัดเจนเพื่อไม่ตีความ effort เป็น automation savings.
- US-005 — ในฐานะ `P-02 Management Reviewer` ฉันต้องการเปิดผลผ่าน browser โดยไม่ต้องอ่าน CSV โดยตรง.
- US-006 — ในฐานะ `P-01 Automation Analyst` ฉันต้องการเปิด task ที่สนใจแล้วขอให้ระบบสร้าง AI Exploration เพื่อรู้ว่าควรตรวจสอบประเด็นใดเพิ่มเติมก่อนตัดสินใจสำรวจ Automation ต่อ.
- US-007 — ในฐานะ `P-01 Automation Analyst` หรือ `P-02 Management Reviewer` ฉันต้องการกลับมาเปิด Exploration Recommendation ที่เคยบันทึกไว้ เพื่อ review เหตุผลและ verification points ภายหลังโดยไม่ต้อง generate ซ้ำ.

## Functional Requirements

| ID | Priority | Requirement |
|---|---|---|
| FR-001 | P0 | ระบบต้องอ่าน `bank_automation_opportunities.csv` ผ่าน ingestion process |
| FR-002 | P0 | ระบบต้อง validate required columns และ row values ก่อน persist |
| FR-003 | P0 | ระบบต้อง persist rows ที่ผ่าน validation ลง SQLite3 |
| FR-004 | P0 | ระบบต้องคำนวณ `weekly_minutes = weekly_runs * minutes_per_run` |
| FR-005 | P0 | ระบบต้องแสดง weekly effort ต่อ task ผ่าน Web UI |
| FR-006 | P0 | ระบบต้องแสดง total weekly effort grouped by `department` |
| FR-007 | P0 | ระบบต้องแสดง Top 3 tasks เรียงจาก `weekly_minutes` มากไปน้อย |
| FR-008 | P0 | ระบบต้องแสดง disclaimer ว่า current effort ไม่ใช่ expected automation savings |
| FR-009 | P0 | ระบบต้อง deploy ผ่าน Coolify และเปิดใช้งานได้ |
| FR-010 | P1 | ระบบอาจเรียก company AI endpoint เพื่อสร้าง exploration recommendation พร้อม rationale และ verification points |
| FR-011 | P1 | AI recommendation ต้องถูก persist และเปิดดูซ้ำบน UI ได้ |

## Non-Functional Requirements

- NFR-001 — production build ต้องสามารถรันใน environment ที่ Coolify deploy ได้.
- NFR-002 — secret/token ต้องไม่อยู่ใน source repository.
- NFR-003 — ingestion ต้อง fail ชัดเจนเมื่อ schema หรือค่าที่จำเป็นไม่ถูกต้อง; ห้าม insert row ที่ invalid แบบเงียบ ๆ.
- NFR-004 — SLO target: `null`; calibration owner: Developer. ต้องวัดจาก deployed application ก่อนกำหนดค่าจริง.
- NFR-005 — coverage threshold: `null`; calibration owner: Developer. ให้มี tests ที่พิสูจน์ calculation/aggregation/validation ก่อน แต่ไม่เดาเปอร์เซ็นต์.
- NFR-006 — AI rate limit/quota: `null`; calibration owner: Platform owner/Developer. โบนัสต้อง handle failure โดยไม่ทำให้ core analytics ใช้งานไม่ได้.

## Acceptance Criteria

- AC-001 (FR-001/002): เมื่อ ingestion อ่านไฟล์ที่มี required columns ครบและค่าถูก type ระบบต้องผ่าน validation; ถ้าขาด required column หรือค่าที่ต้องเป็นจำนวนเต็มใช้ไม่ได้ ต้อง fail พร้อม error ที่ระบุสาเหตุ.
- AC-002 (FR-003): หลัง import สำเร็จ SQLite3 ต้องมี task rows ที่ผ่าน validation และ `task_id` ไม่ซ้ำ.
- AC-003 (FR-004): สำหรับทุก task ค่า weekly effort ต้องเท่ากับ `weekly_runs × minutes_per_run`.
- AC-004 (FR-005): ผู้ใช้เปิดหน้าเว็บแล้วสามารถเห็น `task_id`, `department`, `task_name`, weekly effort ของ task ได้.
- AC-005 (FR-006): department totals บน UI ต้องเท่ากับผล `SUM(weekly_runs * minutes_per_run)` grouped by department จาก DB.
- AC-006 (FR-007): Top 3 ต้องเป็นสาม row ที่มี weekly effort สูงสุดจาก dataset ที่ persist อยู่.
- AC-007 (FR-008): หน้าผลลัพธ์ต้องมีข้อความที่สื่อชัดว่าเวลาที่แสดงเป็น current effort และไม่ใช่เวลาที่ Automation จะประหยัดได้จริง.
- AC-008 (FR-009): production URL บน Coolify ต้องเปิดได้และแสดง core analytics โดยไม่ต้องใช้ไฟล์ CSV ที่เครื่องผู้ประเมิน.
- AC-009 (FR-010/011, bonus): เมื่อ AI call สำเร็จ recommendation ต้องมี recommendation/rationale/verification points ถูก persist และ UI เปิดดูได้; เมื่อ AI call ล้มเหลว core analytics ยังทำงานได้. โดยละเอียด:
  - Task Detail (`/tasks/<task_id>`) ต้องเปิดข้อมูล task จริงจาก DB (task_id, department, task_name, weekly_runs, minutes_per_run, weekly effort ที่คำนวณแล้ว) และแสดง disclaimer เดียวกับ Dashboard.
  - การกด "Generate AI Exploration" ต้องเรียก AI ผ่าน server-side adapter แล้วได้ผลลัพธ์ที่มีครบ `recommendation`, `rationale`, `verification_points`.
  - ผลลัพธ์ต้องถูก persist ลง SQLite3 ก่อนแสดงผล และต้อง reload/refresh หน้าแล้วยังเห็นผลเดิม (ไม่ใช่ state ชั่วคราวใน session/memory).
  - หน้า Saved Explorations (`/explorations`) ต้องแสดงรายการ exploration ที่บันทึกไว้ทั้งหมด พร้อม task, department, weekly effort ตอนที่ generate, และเวลา generate.
  - เมื่อ AI call ล้มเหลวหรือยังไม่ได้ config endpoint, Task Detail ต้องแสดง error/unavailable state ที่ชัดเจน โดย Dashboard, task data, department totals และ Top 3 ต้องยังทำงานถูกต้องตามปกติ.

Validation Checklist
- [x] ทุก FR มี priority จาก `requirement_priority`
- [x] ทุก user story อ้าง persona ID
- [x] มี acceptance criteria ที่ตรวจได้สำหรับ core requirements
- [x] NFR ที่ยังไม่มีค่าจริงใช้ `null` + calibration owner
- [x] ไม่ประกาศ automation savings จาก weekly effort
