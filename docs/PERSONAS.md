# Automation Opportunity Finder — PERSONAS

Project: `Automation Opportunity Finder`  
Document ID: `personas`  
Template: `ddd-web-app-v2.8.0`  
Status: Draft for implementation  

ข้อมูลที่ยืนยันจากโจทย์: ฝ่ายบริหารต้องการข้อมูลเปรียบเทียบเพื่อจัดลำดับว่างานใดควรถูกสำรวจโอกาสทำ Automation ก่อน; ระบบใช้ข้อมูลจาก CSV, ตรวจสอบข้อมูล, จัดเก็บใน SQLite3, และผู้ใช้ต้องเปิดดูผลผ่านหน้าจอได้.  
สมมติฐานที่ต้องยืนยันภายหลัง: ผู้ใช้หลักของหน้าจอเป็นผู้วิเคราะห์/ผู้รับผิดชอบงาน Automation และผู้ใช้รองเป็นผู้บริหารหรือหัวหน้าแผนกที่ใช้ผลเพื่อเลือกงานไปสำรวจต่อ. ระดับ technical skill ด้านล่างเป็น working assumption ไม่ใช่ข้อมูลจากโจทย์.

## Persona Profiles

| Persona ID | Name | Role | Technical Skill | เป้าหมายหลัก |
|---|---|---|---|---|
| P-01 | Automation Analyst (working persona) | ผู้วิเคราะห์หรือผู้รับผิดชอบการสำรวจโอกาสทำ Automation | Medium — assumption | เปรียบเทียบ workload ของงานและแผนกจากข้อมูลชุดเดียว เพื่อหา candidate ที่ควรสำรวจต่อก่อน |
| P-02 | Management Reviewer (working persona) | ผู้บริหารหรือหัวหน้าแผนกที่ใช้ผลประกอบการจัดลำดับการสำรวจ Automation | Low-to-Medium — assumption | เห็นภาพรวมว่าเวลาในปัจจุบันถูกใช้กับงานใดและแผนกใดมาก เพื่อเลือกประเด็นสำหรับการตรวจสอบเชิงลึกต่อ |

## Pain Points

| Persona | Pain Point | Frequency | Current Workaround |
|---|---|---|---|
| P-01 | รายการงานจำนวนมากอยู่ใน CSV แต่ยังไม่ถูกแปลงเป็นข้อมูลเปรียบเทียบที่ใช้จัดลำดับได้ทันที | ทุกครั้งที่ได้รับ dataset สำหรับ review | เปิด CSV แล้วคำนวณ/เรียงข้อมูลด้วยตนเองหรือใช้ spreadsheet ชั่วคราว |
| P-01 | ต้องคำนวณเวลาต่อสัปดาห์จาก `weekly_runs × minutes_per_run` และ aggregate หลายมุมมอง | ทุกครั้งที่วิเคราะห์ชุดข้อมูล | สร้างสูตรและ pivot/summary ใหม่ด้วยมือ |
| P-01 | มีความเสี่ยงตีความ “เวลาที่ใช้ปัจจุบัน” เป็น “เวลาที่ Automation จะประหยัดได้” | ทุกครั้งที่นำผลไปสื่อสาร | อธิบายข้อจำกัดด้วยข้อความประกอบแบบ manual |
| P-02 | ยังไม่มีมุมมองเดียวที่เปรียบเทียบภาระเวลาระหว่างงานและระหว่างแผนกได้ทันที | ทุกครั้งที่ต้องจัดลำดับ candidate | ขอให้ทีมสรุปข้อมูลเป็นรายงานหรือ spreadsheet เพิ่มเติม |
| P-02 | การเห็นงานที่ใช้เวลามากไม่ได้บอกโดยตัวมันเองว่างานนั้นเหมาะกับ Automation | ทุกครั้งที่ใช้ ranking เพื่อประกอบการตัดสินใจ | ขอข้อมูลและเหตุผลเพิ่มจากเจ้าของกระบวนการก่อนตัดสินใจสำรวจต่อ |

## Primary Use Cases

| Persona | Use Case | Trigger | Expected Outcome |
|---|---|---|---|
| P-01 | เปิดดูรายการงานพร้อมเวลาที่ใช้ต่อสัปดาห์ | CSV ตัวอย่างถูก validate และนำเข้า SQLite3 แล้ว | เห็นแต่ละงานพร้อม current weekly effort ที่คำนวณจากข้อมูลต้นทาง |
| P-01 | ตรวจเวลารวมแยกตามแผนก | ต้องเปรียบเทียบ workload ระหว่างหน่วยงาน | เห็นยอดรวมรายแผนกจาก dataset เดียวกัน |
| P-01 | ดู Top 3 งานที่ใช้เวลามากที่สุด | ต้องหา candidate สำหรับสำรวจต่ออย่างรวดเร็ว | เห็น 3 งานที่มี current weekly effort สูงสุดพร้อมข้อมูลอ้างอิงของงาน |
| P-02 | เปิด dashboard เพื่อ review ภาพรวม | ต้องตัดสินใจว่าจะให้ทีมไปสำรวจงานใดก่อน | เห็น task-level, department-level และ Top 3 โดยไม่ต้องเปิด CSV โดยตรง |
| P-02 | ตรวจความหมายของตัวเลขก่อนใช้ตัดสินใจ | เห็น ranking หรือเวลาที่สูง | เห็น disclaimer ชัดเจนว่า current effort ไม่ใช่ expected automation savings |

## Critical Paths

| CP-ID | Persona | Delivery | Critical Action | Failure Impact | Frequency |
|---|---|---|---|---|---|
| CP-01 | P-01 | UI | เห็นเวลาที่ใช้ต่อสัปดาห์ของแต่ละงานจากข้อมูลที่ผ่าน validation และถูกจัดเก็บแล้ว | ไม่สามารถเปรียบเทียบ candidate จากข้อมูลชุดเดียวได้ และต้องย้อนกลับไปคำนวณด้วยมือ | On-demand |
| CP-02 | P-01 | UI | เห็นเวลารวมแยกตามแผนกและ Top 3 งานที่ใช้เวลามากที่สุด | ไม่สามารถจัดลำดับการสำรวจ Automation จากมุมมองภาพรวมและ task-level ได้อย่างรวดเร็ว | On-demand |
| CP-03 | P-02 | UI | เปิดดูผลผ่านหน้าจอและเห็นคำเตือนว่าเวลาที่แสดงเป็น current effort ไม่ใช่เวลาที่ Automation จะประหยัดได้จริง | มีความเสี่ยงใช้ตัวเลขผิดความหมายและสรุป ROI/automation savings โดยไม่มีหลักฐาน | ทุกครั้งที่ review ผล |

Validation Checklist
- [x] ทุก persona มี `name`, `role`, `technical_skill`, pain points, use cases และ critical paths
- [x] CP-ID ไม่ซ้ำกันและเรียงต่อเนื่องในเอกสาร
- [x] ทุก critical path ระบุ Delivery เป็น `UI` หรือ `system`
- [x] ไม่มีการสร้างค่า automation savings จาก current weekly effort
- [x] ไม่มีการใช้ชื่อหรือตัวเลขจาก TaskFlow
- [ ] ยืนยัน persona จริงและ technical skill กับผู้ประเมิน/เจ้าของโจทย์ก่อนถือเป็น final
- [ ] เมื่อสร้าง `UI_SPEC.md` ต้อง trace CP-01 ถึง CP-03 ใน Critical Path Trace
- [ ] เมื่อสร้าง `TESTING.md` ต้องมี E2E scenario ครอบ CP-01 ถึง CP-03
