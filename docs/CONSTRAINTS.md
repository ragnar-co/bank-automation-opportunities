# Automation Opportunity Finder — CONSTRAINTS

Project: `Automation Opportunity Finder`  
Document ID: `constraints`  
Template: `ddd-web-app-v2.8.0`  
Status: Draft for implementation

ข้อมูลที่ยืนยันจากโจทย์: เวลาทำข้อสอบ 120 นาที, คะแนนหลัก 100, โบนัส AI workflow 10, ต้องใช้ CSV ตัวอย่าง, ตรวจสอบข้อมูล, จัดเก็บใน SQLite3 หรือ DuckDB, เปิดผลผ่านหน้าจอ, push เข้า repo บริษัท และ deploy ผ่าน Coolify จนเปิดใช้งานได้, ใช้ Claude Code/Codex และ Token ที่มีอยู่โดยไม่เติมเพิ่ม.  
การตัดสินใจของโปรเจกต์: เลือก `ddd-web-app`, ใช้ SQLite3, ไม่มี CSV Upload UI; ใช้ ingestion/seed process อ่าน CSV ตัวอย่างแทน.

## Legal and Compliance Constraints

- ระบบต้องไม่แสดงหรืออ้างว่า `weekly_time` คือเวลาที่ Automation จะประหยัดได้จริง.
- ระบบต้องใช้ข้อมูลตัวอย่างที่โจทย์ให้เป็นแหล่งข้อมูลของการวิเคราะห์หลัก และห้ามแต่งค่าธุรกิจเพิ่มเพื่อให้ผลดูสมบูรณ์.
- ข้อกำหนดด้าน PDPA/ข้อมูลส่วนบุคคลเฉพาะโปรเจกต์: `null` — calibration owner: Product/Legal reviewer; dataset ที่ได้รับต้องถูกตรวจว่าไม่มีข้อมูลที่ต้องจัดการเพิ่มเติมก่อน production use.

## Technical Constraints

- Input source: `bank_automation_opportunities.csv`.
- Required columns: `task_id`, `department`, `task_name`, `weekly_runs`, `minutes_per_run`.
- Storage: SQLite3.
- Derived metric: `weekly_minutes = weekly_runs * minutes_per_run`.
- CSV ingestion ต้อง validate ก่อน persist.
- Web UI ต้องอ่านผลจากข้อมูลที่ persist แล้ว ไม่ใช่คำนวณจากไฟล์ CSV โดยตรงทุกครั้ง.
- ต้องใช้ Claude Code/Codex ตามเครื่องมือที่โจทย์อนุญาต และใช้ Token ที่มีอยู่เท่านั้น.
- Framework/runtime stack อื่น: `null` — calibration owner: Developer; เลือกจาก environment ที่พร้อมที่สุดในเวลาสอบและบันทึกใน `ARCHITECTURE.md` เมื่อยืนยันแล้ว.

## Security Constraints

- ห้าม commit secret, API token หรือ credential ลง repository.
- AI endpoint credential (ถ้าทำโบนัส) ต้องอ่านจาก environment variable หรือ secret ที่ Coolify จัดการ.
- หน้า core analytics ไม่มีข้อกำหนด authentication จากโจทย์; authentication requirement = `null` — calibration owner: Developer/Exam requirement owner.
- Input validation ต้อง reject row ที่ขาด required field หรือชน type/range rule ก่อน insert.

## Business Constraints

- เวลาทั้งหมดสำหรับ build, verify, push และ deploy: 120 นาที.
- คะแนนหลัก: 100; AI workflow เป็นโบนัส 10 และห้ามทำให้ core deliverable เสี่ยงไม่เสร็จ.
- Core outcome ต้องช่วยจัดลำดับ “โอกาสที่ควรสำรวจต่อ” จาก current weekly effort ไม่ใช่ตัดสิน ROI หรือ automation feasibility แบบฟันธง.
- ต้องเปิดใช้งานได้ผ่าน Coolify ภายในเวลาสอบ.
- SLO, performance budget, coverage threshold, RTO/RPO: `null` — calibration owner: Developer; ไม่ตั้งตัวเลขโดยไม่มีข้อมูลวัดจริง.

## Integration Constraints

- Company Git repository: ต้อง push source และเอกสารที่จำเป็นก่อนส่ง.
- Coolify: ต้อง deploy application จนเปิดใช้งานได้จริง.
- Company AI endpoint (bonus only): ใช้ endpoint และ quota ที่บริษัทจัดให้; quota/rate limit ที่แน่นอน = `null` — calibration owner: Developer/Platform owner.
- AI workflow ต้อง persist recommendation ลงฐานข้อมูลและแสดงบนแอปได้จริง จึงนับว่าปิดโบนัสครบ.

Validation Checklist
- [x] ครบ 5 หมวด constraint ตาม template
- [x] เลือก SQLite3 ชัดเจน
- [x] ไม่มี CSV Upload UI แต่ยังมี CSV ingestion + validation
- [x] ไม่สร้างตัวเลข SLO/coverage/rate limit ขึ้นเอง
- [x] ค่าไม่ทราบใช้ `null` พร้อม calibration owner
- [x] แยก core requirement ออกจาก AI bonus
