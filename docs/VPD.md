# Automation Opportunity Finder — VPD

Project: `Automation Opportunity Finder`  
Document ID: `vpd`  
Template: `ddd-web-app-v2.8.0`  
Status: Draft for implementation  
Depends on: `personas`, `constraints`

## Customer Profile

Primary customer profile: ผู้วิเคราะห์/ผู้รับผิดชอบการสำรวจโอกาสทำ Automation และผู้บริหารที่ต้องใช้ข้อมูลเปรียบเทียบเพื่อเลือกงานไปสำรวจต่อ.

## Customer Jobs

- เปรียบเทียบเวลาที่ใช้ต่อสัปดาห์ของงานจำนวนมากจาก dataset เดียวกัน.
- เห็นภาระเวลารวมของแต่ละแผนก.
- หา candidate ที่ควรถูกสำรวจ Automation ก่อนจาก signal ที่ตรวจสอบย้อนกลับได้.
- สื่อสารผลโดยไม่ทำให้ผู้รับสารเข้าใจผิดว่า current effort คือ automation savings.

## Pains

- CSV มีข้อมูลจำนวนมากและไม่สะดวกต่อการจัดลำดับด้วยตา.
- การคำนวณ `weekly_runs × minutes_per_run` และ aggregate ซ้ำด้วยมือเสียเวลาและเสี่ยงผิดพลาด.
- ฝ่ายบริหารไม่มีมุมมองเปรียบเทียบงานและแผนกในหน้าจอเดียว.
- งานที่ใช้เวลามากอาจถูกเข้าใจผิดว่า “ประหยัดได้มาก” ทั้งที่ยังไม่มีข้อมูล feasibility หรือ exception rate.

## Gains

- ได้ ranking ที่คำนวณจากสูตรเดียวกันทั้งระบบ.
- เห็น department totals และ Top 3 ได้ทันที.
- ย้อนกลับไปหา task ต้นทางได้ด้วย `task_id`.
- รู้ข้อจำกัดของตัวเลขก่อนนำไปใช้ตัดสินใจ.

## Value Map

ระบบรับ CSV ตัวอย่างผ่าน ingestion process, validate และ persist ลง SQLite3 แล้วให้ Web UI แสดง task-level weekly effort, department totals และ Top 3 พร้อม disclaimer ที่ชัดเจน.

## Pain Relievers

- Validation ลดความเสี่ยงจาก schema/type ที่ผิดก่อนข้อมูลเข้า DB.
- Query จาก SQLite3 ทำให้ calculation/aggregation มีแหล่งข้อมูลเดียว.
- Dashboard ลดงานสรุป CSV ด้วยมือ.
- Disclaimer ป้องกันการตีความ `weekly_minutes` เป็น expected savings.

## Gain Creators

- Top 3 ทำให้เห็น candidate สำหรับการสำรวจต่ออย่างรวดเร็ว.
- Department totals ช่วยเห็น concentration ของ effort ระดับหน่วยงาน.
- ถ้าทำโบนัส AI ระบบสามารถสร้าง “ข้อเสนอเพื่อสำรวจต่อ” พร้อมเหตุผลและสิ่งที่ต้องตรวจสอบ โดย persist ผลไว้ดูซ้ำได้.

## Value Propositions

- เปลี่ยนรายการงานจาก CSV ให้เป็นข้อมูลเปรียบเทียบที่ใช้จัดลำดับการสำรวจ Automation ได้ผ่าน Web UI.
- ให้ current weekly effort เป็น signal ที่โปร่งใสและคำนวณย้อนกลับได้ โดยไม่อ้างเป็น automation savings.
- เสริม AI ได้ภายหลังเพื่อช่วยตั้งสมมติฐานการสำรวจ ไม่ใช่แทนการตรวจสอบ feasibility จริง.

Validation Checklist
- [x] มี customer jobs, pains, gains, pain relievers, gain creators และ value propositions
- [x] เนื้อหา derive จาก PERSONAS.md และโจทย์ ไม่สร้าง persona ใหม่
- [x] ไม่แปลง weekly effort เป็น savings estimate
- [x] AI bonus ถูกวางเป็น optional value add ไม่ใช่ core dependency
