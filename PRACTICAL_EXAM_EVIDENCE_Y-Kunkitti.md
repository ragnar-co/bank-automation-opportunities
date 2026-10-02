# PRACTICAL_EXAM_EVIDENCE_Y-Kunkitti

รายงานหลักฐานการทำงาน (Practical Exam) — สร้างขึ้นเพื่อประกอบการให้คะแนนและ feedback โดยกรรมการ
เอกสารนี้สร้างขึ้น**หลังช่วงทำงานในบทสนทนา** ตามคำสั่งตรวจสอบที่ได้รับ ไม่ใช่เอกสารที่ร้องขอโดยผู้สอบในฐานะส่วนหนึ่งของงานส่งสอบ

**หมายเหตุสำคัญก่อนเริ่มอ่าน (อัปเดต):** คำสั่งที่ใช้สร้างรายงานนี้ระบุไว้ชัดเจนในข้อสุดท้ายว่า "อย่า commit, push หรือ deploy รายงาน" และให้สร้างไฟล์ไว้นอก repo ในโฟลเดอร์ข้างเคียง ผู้จัดทำรายงาน (AI assistant) สร้างไฟล์ไว้นอก repo ตามกติกานั้นก่อน และได้แจ้งข้อขัดแย้งนี้ให้ผู้ใช้ทราบแล้ว 2 ครั้ง

หลังจากนั้น **ผู้ใช้ซึ่งเป็นเจ้าของ repo ยืนยันโดยตรงและชัดเจนซ้ำ 3 ครั้ง** ให้นำไฟล์นี้เข้า repo แล้ว commit/push — ผู้จัดทำรายงานจึงดำเนินการตามคำสั่งตรงของเจ้าของ repo โดยถือว่าเป็นการ **override กติกา "ห้าม commit/push" ของ audit protocol ข้างต้นอย่างชัดแจ้งและจงใจโดยผู้มีอำนาจตัดสินใจเหนือ repo นี้จริง** ไม่ใช่การเพิกเฉยต่อกติกาโดยพลการของ AI assistant เอง

**ผลคือ:** ไฟล์รายงานนี้ **ถูก commit และ push เข้า repo งานสอบแล้ว** ซึ่งหมายความว่า ณ จุดนี้เป็นต้นไป repo มี commit ที่เกิดขึ้น **หลังช่วงเวลาทำงานที่รายงานนี้บรรยายถึง** ปะปนอยู่ในประวัติ — กรรมการควรพิจารณา commit ที่มีไฟล์นี้ (และ commit ใดๆ หลังจากนั้น) แยกต่างหากจากสิ่งที่ถือเป็น "งานที่ส่งสอบจริง" โดยอ้างอิง commit SHA ที่ระบุไว้ในหัวข้อ B/E001 เป็นขอบเขตของงานสอบ ไม่ใช่ HEAD ที่รวมไฟล์นี้

---

## 0. ข้อมูลการรวบรวมหลักฐาน (บันทึกก่อนสร้างรายงาน)

| รายการ | ค่าที่พบ |
|---|---|
| เวลาที่เริ่มรวบรวมหลักฐาน | 2026-10-02 12:06:52 (UTC+07:00 ตาม offset ของเครื่องที่รัน; ไม่มีหลักฐานยืนยันชื่อ timezone/เขตเวลาอย่างเป็นทางการ) |
| คำสั่งที่ใช้อ่านเวลา | `date` และ `date +%Z` รันบนเครื่อง local ที่ใช้ทำงาน |
| Repo root | `/Users/kunkittimacbook/Downloads/bank_automation_opportunities` |
| Branch | `main` |
| HEAD commit SHA (ตอนรวบรวม) | `6e10f3cacd916d2e84eb962ef558befd8fff3620` |
| ความสัมพันธ์กับ remote | `main` ตรงกับ `origin/main` เป๊ะ (`branch.ab +0 -0`) — ไม่มี commit ที่ unpush |
| Working tree ตอนรวบรวม | สะอาด ยกเว้นไฟล์ untracked 1 ไฟล์: `README.md` |

**สภาพที่พบตอนรวบรวม** ≠ **สภาพที่ยืนยันได้ว่าเป็นช่วงสอบ**: ไม่มีหลักฐานใน session ที่ระบุเวลาเริ่ม/หมดเวลาสอบอย่างเป็นทางการ (ไม่มี timer, ไม่มีประกาศ "เริ่มสอบ"/"หมดเวลา" ปรากฏเป็นข้อความจากผู้ใช้หรือระบบ) จึงระบุเวลาสอบจริงเป็น **UNKNOWN** — ดูเหตุผลในหัวข้อ A

---

## A. ข้อมูลผู้สอบและขอบเขตหลักฐาน

### ผู้สอบ
- **ชื่อที่ใช้ตั้งชื่อไฟล์:** `Y-Kunkitti` — มาจาก `git config user.name` ของ commit ทั้งหมดใน repo นี้ (VERIFIED, E001)
- ข้อมูลระบุตัวตนอื่นที่พบในบริบท ซึ่ง **ไม่ตรงกันเป๊ะ** และไม่มีข้อความใดในบทสนทนาระบุ "ชื่อเต็ม" ของผู้สอบโดยตรง จึงไม่เลือกยืนยันชื่อใดชื่อหนึ่งเป็น "ชื่อจริง":
  - `git config user.email` ของทุก commit = `kittiphongyimsaard@gmail.com` (อีเมลส่วนตัว, VERIFIED, E001)
  - อีเมลที่ระบบ host แจ้งมาในบริบท session (`userEmail` metadata) = `kittiphong@ragnar.co.th` (อีเมลบริษัท, REPORTED จาก system context ไม่ใช่จากไฟล์ repo)
  - ตำแหน่ง/แผนก: ไม่พบระบุไว้ที่ใดในบทสนทนาหรือไฟล์ repo → **UNKNOWN**

### โจทย์ DDD ที่เลือก
- Template: `ddd-web-app-v2.8.0` (พบระบุใน header ของทุกไฟล์ `docs/*.md`, VERIFIED, E010)
- โจทย์: "Automation Opportunity Finder" — แอปแปลง CSV งานซ้ำรายสัปดาห์เป็นข้อมูลจัดลำดับโอกาสสำรวจ Automation พร้อมโบนัส AI workflow (พบใน `docs/CONSTRAINTS.md:8`, VERIFIED, E018)

### เครื่องมือที่ใช้
- Claude Code (AI coding agent) เป็นเครื่องมือหลักตลอด session — ยืนยันจากการที่ทุก commit message มี trailer `Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>` (VERIFIED, E001)
- coolify-cli ผ่าน SSH ไปยังเซิร์ฟเวอร์ `hera2` สำหรับ deploy (REPORTED+VERIFIED บางส่วน — ดูหัวข้อ I)
- Docker / Docker Compose บนเครื่อง local (VERIFIED จาก build/run log ที่ปรากฏใน session tool output)
- OpenRouter เป็น AI endpoint สำหรับฟีเจอร์โบนัส (VERIFIED จาก ADR-005 และ session tool-call output)

### Repo / URL แอป
- Repo: `https://github.com/ragnar-co/bank-automation-opportunities.git` (VERIFIED, `git remote -v`, E001)
- Production URL (ตามที่ Coolify สร้างให้): `http://hnvwwlptzqituru34ckd44kv.hera2.ragnar-ai.dev` — **REPORTED+VERIFIED บางส่วนในขอบเขต session เท่านั้น** (ดูหัวข้อ I — ไม่สามารถตรวจซ้ำได้เพราะกติกาห้ามเรียกบริการภายนอกเพิ่มในการรวบรวมหลักฐานครั้งนี้)

### แหล่งข้อมูลที่เข้าถึงได้ในการรวบรวมหลักฐานนี้
1. ประวัติบทสนทนาและผลลัพธ์ tool-call ที่ปรากฏใน session ปัจจุบัน (ตั้งแต่ต้น session ที่มองเห็นได้ — **ไม่ยืนยันว่าเป็นบทสนทนาทั้งหมดของการสอบ** เพราะระบบอาจมีการสรุป/ตัดทอนบทสนทนาส่วนต้นมาก่อนหน้านี้ ตาม mechanism "context summarization" ที่ระบุไว้ในระบบ)
2. ไฟล์ปัจจุบันใน working tree ของ repo
3. `git log`, `git show`, `git status`, `git diff` (คำสั่งอ่านอย่างเดียว รันระหว่างรวบรวมหลักฐานนี้)

### แหล่งข้อมูลที่ขาดหรือเข้าถึงไม่ได้
- **ไม่มีหลักฐานเวลาสอบอย่างเป็นทางการ** (เวลาเริ่ม/หมดเวลา) — มีเพียง timestamp ของ git commit ซึ่งเป็นเวลาที่เครื่อง local บันทึกไว้เท่านั้น
- **ไม่สามารถตรวจสอบสถานะ Coolify/production URL ซ้ำได้ ณ ขณะสร้างรายงานนี้** เพราะกติกาห้าม fetch/pull หรือเรียกบริการภายนอกเพิ่มเติม — ใช้ได้เฉพาะผลที่สังเกตได้ในบทสนทนาก่อนหน้าเท่านั้น
- **ไม่มีหลักฐานอิสระ (เช่น CI log, screenshot ที่ประทับเวลาจากบุคคลที่สาม)** ยืนยันว่า push/deploy เกิดขึ้น "ทันเวลาสอบ" เพราะไม่ทราบเวลาสอบที่แน่ชัด
- ไม่พบไฟล์ใด ๆ ที่ระบุชื่อเต็มผู้สอบ, เลขที่ผู้สอบ, หรือรหัสการสอบ

---

## B. สภาพงานที่พบ

- **Branch:** `main`
- **HEAD (ตอนรวบรวม):** `6e10f3cacd916d2e84eb962ef558befd8fff3620`
- **Commit ที่ "ส่งสอบ" อย่างเป็นทางการ:** ไม่มีหลักฐานแยกต่างหากในบทสนทนาที่ระบุชัดว่า "นี่คือ commit ที่ส่งสอบ" (ผู้สอบไม่เคยพิมพ์ข้อความลักษณะนั้น) จึงใช้ HEAD ล่าสุดที่ push สำเร็จ (`6e10f3c`) เป็นข้อมูลอ้างอิง โดยระบุชัดว่าเป็น **INFERRED** ไม่ใช่ VERIFIED ว่าตรงกับ "commit ที่ส่งสอบ"
- **สถานะ working tree ก่อนสร้างรายงานนี้:** สะอาด, untracked ไฟล์เดียวคือ `README.md`

### งานที่อยู่ใน commit (5 commits ทั้งหมด อยู่ใน `main` และ push ไปยัง `origin/main` แล้วทุก commit — VERIFIED, E001, E003)

| Commit | เวลา (local, UTC+07:00) | สรุปเนื้อหา |
|---|---|---|
| `47dfaba` | 2026-10-02T10:36:55+07:00 | เพิ่มไฟล์ CSV ตัวอย่าง (`bank_automation_opportunities.csv`, 12,419 แถวข้อมูล + 1 header) |
| `64168c5` | 2026-10-02T10:57:24+07:00 | Core MVP: Flask app, SQLite schema, CSV import script, dashboard, เอกสาร DDD ชุดแรก (CONSTRAINTS, PERSONAS, VPD, SCOPE, PRD, ARCHITECTURE, GLOSSARY), tests เริ่มต้น |
| `37ffca8` | 2026-10-02T11:33:35+07:00 | เพิ่มฟีเจอร์ AI Exploration (bonus), ปรับโครงสร้างเป็น `app/` package, เพิ่มเอกสาร ADR/DATA_MODEL/UI_SPEC, เพิ่ม Docker Compose |
| `cd86c3c` | 2026-10-02T11:41:51+07:00 | แก้ปัญหา port ชนกันบน Coolify (`ports` → `expose`) |
| `6e10f3c` | 2026-10-02T12:02:26+07:00 | ปรับ UI ใหม่เป็นธีมมืด "Ledger Noir" พร้อม animation, อัปเดตเอกสารให้ตรงความจริง, เพิ่ม ADR-006 |

(ที่มา: `git log --all --date=iso-strict`, VERIFIED, Evidence ID **E001**)

### งานที่ยังไม่ commit / ไฟล์ที่ไม่ทราบที่มาแน่ชัด

| ไฟล์ | สถานะ | หมายเหตุ |
|---|---|---|
| `README.md` | Untracked (ยังไม่ add/commit) | สร้างขึ้นในบทสนทนาเดียวกันนี้ **ก่อน** ที่คำสั่งตรวจสอบหลักฐานนี้จะถูกส่งเข้ามา แต่ยังไม่ได้ถูก commit หรือ push ณ เวลาที่รวบรวมหลักฐาน จึง**ไม่นับเป็นส่วนหนึ่งของ commit ที่ส่งสอบ** |

**ไม่ถือว่าไฟล์ทั้งหมดใน repo ถูกสร้างระหว่างสอบโดยอัตโนมัติ** — ไฟล์ที่ไม่อยู่ใน commit ใด ๆ (เช่น `README.md`) ถือเป็นงานที่เกิดขึ้นหลัง/นอกเหนือจาก commit ที่ push ไปแล้ว

---

## C. ลำดับการทำงาน

หมายเหตุ: ไม่มี timestamp ระดับนาทีสำหรับทุกขั้นตอนย่อยในบทสนทนา (มีเฉพาะ timestamp ของ git commit) จึงเรียงตามลำดับก่อน-หลังที่ปรากฏใน session และอ้างอิงเวลา commit เมื่อมี ไม่มีการกะประมาณเวลาที่ใช้ในแต่ละขั้นตอนขึ้นเอง

| ลำดับ | เวลา/ช่วงเวลา | สิ่งที่ทำ | ผู้ดำเนินการที่ยืนยันได้ | ผลที่พบ | Evidence ID |
|---|---|---|---|---|---|
| 1 | ก่อน 10:36 (ไม่ทราบเวลาเริ่มแน่ชัด) | รับโจทย์, สร้าง GitHub repo `ragnar-co/bank-automation-opportunities` (private), commit ไฟล์ CSV | ผู้สอบสั่งงานผ่านข้อความ, AI assistant (Claude Code) เป็นผู้รัน git commands จริง | Repo ถูกสร้าง, CSV ถูก commit | E001, E002 |
| 2 | 10:36–10:57 | เขียน CLAUDE.md, เอกสาร DDD ชุดแรก (CONSTRAINTS/PERSONAS/VPD/SCOPE/PRD/ARCHITECTURE/GLOSSARY) ตาม template `ddd-web-app`, ออกแบบ schema `tasks`, implement Flask app + SQLite + CSV import script + dashboard, เขียน tests, รัน CSV import จริงกับไฟล์ตัวอย่าง (12,419/12,419 แถว, reject 0), รัน pytest, commit | AI assistant ดำเนินการตามคำสั่งผู้สอบในบทสนทนา | Commit `64168c5` | E001, E010 |
| 3 | 10:57–11:33 | เพิ่ม AI Exploration (bonus): ออกแบบ schema `exploration_recommendations`, เขียน `ai_service.py` adapter, ปรับโครงสร้างเป็น `app/` package, เขียนเอกสาร ADR/DATA_MODEL/UI_SPEC, ทดสอบเชื่อมต่อ OpenRouter จริงด้วย API key ที่ผู้สอบให้มา (ชั่วคราว 24 ชม.), แก้บั๊กจริงที่พบระหว่างทดสอบ (markdown code-fence ในผล AI, คำว่า "ROI" หลุดมาในข้อความ AI), รัน Docker local test, commit | AI assistant ดำเนินการ, ผู้สอบเป็นผู้ให้ API key ในบทสนทนา | Commit `37ffca8` | E001, E007, E009 |
| 4 | 11:33–11:41 | ทดลอง deploy ผ่าน coolify-cli (SSH ไป `hera2`): สร้าง project, สร้าง app (docker-compose build pack), ตั้งค่า env vars, deploy — พบปัญหา port ชนกับ dashboard ของ Coolify เอง, แก้ไข `docker-compose.yaml` (`ports`→`expose`) และเพิ่ม `docker-compose.override.yml`, redeploy, commit | AI assistant ดำเนินการผ่าน SSH/coolify-cli ตามคำสั่งผู้สอบ | Commit `cd86c3c`; deployment status "finished" (session tool output) | E001, E014 |
| 5 | 11:41–11:4x | แก้ปัญหา domain/Traefik routing เพิ่มเติม (ports_exposes ถูกรีเซ็ตเป็น 80, domain field ถูกล้างค่า) ผ่านการเรียก Coolify API โดยตรงด้วย token ของ CLI เอง, ยืนยันว่า route ผ่าน Traefik ได้ 200 OK | AI assistant | Traefik routing ยืนยันทำงานถูกต้อง (session tool output) | E014 |
| 6 | 11:41–12:02 | ปรับ UI/UX ใหม่ทั้งหมดเป็นธีมมืด "Ledger Noir" (design tokens, font, animation), ทดสอบด้วย Playwright, แก้บั๊ก UI ที่พบ (ลูกศรซ้อน, CSS รั่วข้ามตาราง), อัปเดตเอกสารให้ตรงความจริง (เพิ่ม ADR-006), commit | AI assistant ตามคำสั่งผู้สอบ | Commit `6e10f3c` | E001, E010 |
| 7 | หลัง 12:02 (ไม่ทราบเวลาแน่ชัด) | เขียน `README.md` (ยังไม่ commit), รัน local dev server ให้ผู้สอบดู | AI assistant | ไฟล์ `README.md` untracked ณ เวลารวบรวมหลักฐาน | E002 |
| 8 | ระหว่างรวบรวมหลักฐานนี้ | ผู้สอบส่งคำสั่งตรวจสอบและรวบรวมหลักฐานสอบ (คำสั่งที่กำลังปฏิบัติอยู่นี้) | ผู้สอบ (อ้างว่าเป็นคำสั่งจากผู้คุมสอบ) | สร้างรายงานนี้ | — |

---

## D. คำสั่งและเครื่องมือที่ใช้ระหว่างสอบ

หมวดนี้สรุปจากประเภทคำสั่งที่ปรากฏใน session เท่านั้น (ไม่ใช่ log แบบ raw ทุกบรรทัด เพื่อความกระชับ) — ระบุชัดว่าเป็นการสรุป

### 1. คำสั่งที่มีหลักฐานว่า execute แล้วจริง (บางส่วน)

| ลำดับ | คำสั่ง/tool ที่พบ | จุดประสงค์ที่มีหลักฐาน | ผล/exit code ที่พบ | ช่วงเวลา | Evidence ID |
|---|---|---|---|---|---|
| 1 | `gh repo create ragnar-co/bank-automation-opportunities --private ...` | สร้าง repo | สำเร็จ, ได้ URL repo | ต้น session | E003 (git remote สอดคล้อง) |
| 2 | `git add`, `git commit -m "..."`, `git push` (ทำซ้ำ 5 รอบ) | บันทึกและส่งงานขึ้น remote | สำเร็จทุกครั้ง (local/remote SHA ตรงกัน) | สอดคล้องกับ 5 commit timestamps | E001, E003 |
| 3 | `.venv/bin/python scripts/import_csv.py` | นำเข้าข้อมูล CSV → SQLite | พบผล "Rows read: 12419, Imported rows: 12419, Rejected rows: 0" ใน session output (DURING_EXAM) | ระหว่างขั้นตอน C.2 และซ้ำอีกหลายครั้งหลังจากนั้นเพื่อ reset DB ทดสอบ | E004 |
| 4 | `.venv/bin/python -m pytest -q` (ทำซ้ำหลายรอบตลอด session) | รัน automated tests | ผลล่าสุดที่สังเกตได้ใน session คือ "28 passed" | ซ้ำหลายครั้งตลอด C.2–C.6 | E009 |
| 5 | `docker build` / `docker compose up --build` | ทดสอบ container ที่จะ deploy จริง | build สำเร็จ, container "healthy" ตาม healthcheck | ช่วง C.3–C.4 | E013 |
| 6 | `ssh hera2 "coolify ..."` (หลายคำสั่งย่อย: `project create`, `app create github`, `app env update`, `app update --ports-exposes`, `deploy uuid --force`) | สร้างและ deploy แอปบน Coolify | รายละเอียดผลแยกในหัวข้อ I | ช่วง C.4–C.5 | E014 |
| 7 | คำเรียก OpenRouter API โดยตรง (ผ่าน `curl`/`requests` ในคำสั่งทดสอบ) | ทดสอบ AI endpoint จริงก่อนเชื่อมเข้าแอป | ได้ผล JSON ที่มี `recommendation`/`rationale`/`verification_points` สำเร็จอย่างน้อย 1 ครั้งที่ไม่มีคำต้องห้าม | ช่วง C.3 | E007, E015 |
| 8 | Playwright browser automation (`browser_navigate`, `browser_take_screenshot`) | ตรวจสอบ UI ด้วยภาพจริงในเบราว์เซอร์ | พบ screenshot และ snapshot หลายจุดตลอด session (ไฟล์ภาพถูกลบทิ้งหลังตรวจสอบเสร็จในแต่ละรอบ — ไม่ได้ถูก commit) | ช่วง C.2, C.6 | — (REPORTED จาก session, ไฟล์ภาพไม่หลงเหลือให้ตรวจซ้ำ) |

### 2. คำสั่งที่เพียงเสนอหรือกล่าวถึง (ไม่มีหลักฐานว่า execute)

- คำแนะนำให้เพิ่ม `--workers` ให้ Gunicorn เพื่อแก้ปัญหา single-worker blocking — **มีการเสนอและอธิบายไว้ แต่ไม่มีหลักฐานว่าถูกนำไปแก้ไขจริงใน source code** (ดูหัวข้อ F)
- การปิด Cloudflare "Always Use HTTPS" ที่ edge — ผู้สอบเลือก "ปล่อยไว้แบบนี้" จึงไม่มีการดำเนินการใด ๆ

### 3. คำสั่งอ่านอย่างเดียวที่ใช้รวบรวมรายงานฉบับนี้ (AFTER_EXAM)

`date`, `pwd`, `git rev-parse --show-toplevel`, `git branch --show-current`, `git rev-parse HEAD`, `git remote -v`, `git config user.name`/`user.email`, `git log --all --date=iso-strict --pretty=...`, `git log --all --stat`, `git status --porcelain=v2 --branch`, `git rev-parse main origin/main`, `git log --oneline origin/main`, `grep`/`wc -l` บนไฟล์ source และเอกสารใน repo, `git log --all -p | grep -c "sk-or-v1"` (ตรวจสอบว่าไม่มี secret หลุดใน git history — ผลลัพธ์ = 0)

ไม่มีการรัน `pytest`, `docker`, `python scripts/import_csv.py`, `app.run`, หรือคำสั่ง deploy ใด ๆ ซ้ำในขั้นตอนรวบรวมหลักฐานนี้

---

## E. การตัดสินใจและการใช้ AI

### การเลือก DDD / stack / DB / ขอบเขต (พบหลักฐานเป็นเอกสาร ADR จริงใน repo)

| การตัดสินใจ | เหตุผลที่ปรากฏในหลักฐาน | ที่มา |
|---|---|---|
| ใช้ template `ddd-web-app` ไม่ใช่ `ddd-data-analytics` | ไม่พบเหตุผลเจาะจงเขียนไว้แยกต่างหาก (เป็นการเลือกตั้งแต่ก่อนที่จะเห็นบทสนทนาส่วนต้น) | UNKNOWN (ที่มาของการเลือกไม่ปรากฏในหลักฐานที่เข้าถึงได้) |
| Flask + server-rendered Jinja แทน SPA | "repo ว่างตอนเริ่ม, ไม่มี frontend framework เดิม, โจทย์ต้องการ dashboard ง่าย ไม่ใช่ SPA ซับซ้อน" | `docs/ADR.md` ADR-001 (VERIFIED) |
| SQLite3 แทน DuckDB | dataset เล็ก, bonus ต้องมี write-back (persist AI recommendations) ในที่เก็บเดียวกับข้อมูลหลัก | `docs/ADR.md` ADR-002 (VERIFIED) |
| ไม่ persist `weekly_minutes` เป็นคอลัมน์ | ป้องกัน derived column ค้างค่าเก่าถ้า source values เปลี่ยน | `docs/ADR.md` ADR-003 (VERIFIED) |
| แยก AI call ไว้ใน `ai_service.py` module เดียว | กัน AI ล้มแล้วกระทบ core analytics, ทดสอบได้โดยไม่ต้องใช้ quota จริง | `docs/ADR.md` ADR-004 (VERIFIED) |
| ใช้ OpenRouter เป็น stand-in ชั่วคราวแทน endpoint บริษัท | endpoint บริษัทจริงยังไม่พร้อม, บริษัทออก API key ชั่วคราว (24 ชม.) ให้ทดสอบแทน | `docs/ADR.md` ADR-005 (VERIFIED code+doc), ที่มาของ key: REPORTED จากข้อความผู้สอบในบทสนทนา |
| `docker-compose.yaml` ใช้ `expose` ไม่ใช่ `ports` | ป้องกัน host-port ชนกันบน Coolify ที่เป็น shared host (ชนกับ dashboard ของ Coolify เองจริงตอนทดสอบ deploy) | `docs/ADR.md` ADR-006 (VERIFIED) |
| ไม่สร้างฟีเจอร์ CSV upload UI, ไม่คำนวณ automation score/estimated savings/ROI | ไม่มีข้อมูลรองรับการคำนวณ, โจทย์ห้ามอ้างว่า weekly effort คือ savings | `docs/SCOPE.md`, `docs/CONSTRAINTS.md` (VERIFIED) |

### หลักฐานการตรวจ/ปรับ output ของ AI โดยผู้สอบ

- พบว่า**ผู้สอบเป็นผู้ให้ข้อมูลโจทย์ต้นฉบับ** (ข้อความโจทย์เต็มที่ตรงกับ `docs/CONSTRAINTS.md`) และ**เป็นผู้ให้ค่า configuration จริง** เช่น ชื่อ model ที่ต้องการ (`anthropic/claude-sonnet-4.6`) และ API key — แสดงถึงการมีส่วนร่วมในการกำหนดทิศทาง
- พบคำถามเชิงตรวจสอบจากผู้สอบในบทสนทนา เช่น การถามถึงพฤติกรรมของ "Saved Explorations" และการถามเรื่อง HTTP/HTTPS ของ domain ก่อนตัดสินใจ — บ่งชี้ว่ามีการอ่าน/ตรวจสอบผลงานก่อนตอบรับ
- **ไม่มีหลักฐานโดยตรง** ที่แสดงว่าผู้สอบอ่าน/แก้ไข source code ด้วยตนเอง (เช่น การแก้ไฟล์โดยไม่ผ่าน AI assistant) — คำสั่งแก้ไขไฟล์ทั้งหมดที่พบถูกดำเนินการโดย AI assistant ตามคำสั่งในบทสนทนา
- **ไม่สามารถสรุปได้**จากหลักฐานที่มีว่าผู้สอบ "เข้าใจ" หรือ "ไม่เข้าใจ" โค้ดที่ AI สร้างให้ในเชิงลึก — ไม่มีหลักฐานเพียงพอสำหรับข้อสรุปเชิงนี้ จึงไม่ฟันธง (ตามกติกาข้อ 3)

### Token/quota

- พบหลักฐาน quota ของ OpenRouter API key ที่ใช้ทดสอบ ณ ขณะตรวจสอบครั้งหนึ่งระหว่างการพัฒนา: `limit: 5, limit_remaining: 5, usage: 0, expires_at: 2026-10-03T04:11:23.267Z` (หน่วยเป็น USD ตาม field name ของ OpenRouter API) — เป็นค่า ณ จุดเวลาที่ตรวจครั้งเดียวเท่านั้น **ไม่มีหลักฐานยอดใช้จริงสะสมหรือยอดคงเหลือล่าสุด ณ สิ้นสุด session** จึงไม่ประมาณการยอดใช้ต่อ
- ไม่พบหลักฐานการใช้ quota ของ Claude Code/Codex (จำนวน token ที่ใช้ในการสนทนา/เขียนโค้ด) ในหลักฐานที่เข้าถึงได้ → UNKNOWN

---

## F. ปัญหาและสิ่งที่ติด

| ปัญหา | อาการ/error ที่พบ | วิธีที่ลอง | ผลที่ยืนยันได้ | ยังไม่ทราบ/ยังค้าง | Evidence ID |
|---|---|---|---|---|---|
| Host port ชนกันบน Coolify | `Error response from daemon: ... Bind for 0.0.0.0:8000 failed: port is already allocated` ตอน deploy ครั้งแรก | ตรวจสอบด้วย `docker ps` พบว่า container ชื่อ `coolify` เองใช้ host port 8000 อยู่ก่อน, แก้ `docker-compose.yaml` จาก `ports` เป็น `expose`, เพิ่ม `docker-compose.override.yml` สำหรับ local | Deploy รอบถัดไปผ่าน (`finished` status), container ขึ้นเป็น `healthy` | — | E014, commit `cd86c3c` |
| `--ports-exposes` ของ coolify-cli ถูกรีเซ็ตเป็น `80` หลังสร้าง app | Traefik label ที่ generate มาชี้ port 80 แต่ container ฟังที่ 8000 จริง | รัน `coolify app update --ports-exposes 8000` และเปิด health check ที่ `/health` | ยืนยันค่าถูกแก้เป็น 8000 ใน `app get` (session output) | **ยังไม่ชัดว่าเป็นบั๊กของ coolify-cli เวอร์ชันที่ใช้ (1.6.2) หรือพฤติกรรมที่ตั้งใจ** — ไม่มีการตรวจสอบเพิ่มเติม | E014 |
| คำสั่ง `app update` ไปล้างค่า `domains` ของ app โดยไม่ตั้งใจ | หลังรัน update, field `domains` กลายเป็น `null`, Traefik routing คืนค่า 404 | ตั้งค่าใหม่ผ่าน field เฉพาะของ compose app คือ `docker_compose_domains` โดยเรียก Coolify REST API ตรง (ผ่าน token เดียวกับ CLI) เนื่องจาก CLI ไม่มี flag รองรับ field นี้ | Routing ผ่าน Traefik กลับมาทำงาน (ทดสอบ 200 OK ผ่าน `docker exec coolify-proxy wget ...`) | **เป็นข้อจำกัดของ coolify-cli ที่ไม่ expose field `docker_compose_domains` — ยังไม่มีการรายงาน/แก้ไขที่ต้นทาง** | E014 |
| โมเดล AI (ผ่าน OpenRouter) ใส่คำว่า "ROI" ในข้อความแม้มี system prompt ห้ามไว้แล้ว | พบข้อความจริงจากการทดสอบ 1 ครั้ง: "ROI on automation investment would likely be achieved within weeks..." | เพิ่ม content-guard ตรวจคำต้องห้ามในข้อความ (ไม่ใช่แค่ชื่อ field) ที่ `app/ai_service.py` | มี unit test ยืนยันพฤติกรรม reject (`tests/test_ai.py`) — **แต่ไม่มีหลักฐานการรันทดสอบซ้ำกับ production endpoint จริงหลังแก้ไข เพื่อยืนยันว่า guard นี้ทำงานกับ response จริงเสมอ (มีความเสี่ยงที่โมเดลจะใช้คำพ้องความหมายอื่นที่ guard ตรวจไม่เจอ)** | E007, `tests/test_ai.py` |
| Gunicorn รันด้วย single sync worker (default) | พบจาก log: "Booting worker with pid: 8" (worker เดียว); สังเกตได้ว่า request อื่นค้างระหว่างที่ worker กำลังรอ AI endpoint ตอบกลับ | มีการ**เสนอ**ให้เพิ่ม `--workers` แต่ผู้สอบตอบว่า "ไม่ต้องหรอก ตอนนี้ เอาขึ้น git ไป deploy ก่อน" | **ยังไม่ได้แก้ไข** — ยืนยันจากการตรวจ `Dockerfile` ปัจจุบัน (CMD ไม่มี `--workers`) | ปัญหานี้**ยังคงอยู่ในโค้ดที่ push ล่าสุด** ยังไม่ถูกแก้ | Dockerfile (tracked, HEAD `6e10f3c`) |
| ไม่สามารถตรวจสอบ URL production ผ่าน `curl` ธรรมดาได้ | Cloudflare คืน `403` (bot-challenge page) สำหรับ `curl`, และ `301` redirect ไป HTTPS เมื่อใช้ browser user-agent | ทดสอบตรงที่ container/Traefik แทน (bypass Cloudflare) ผ่าน `docker exec` | ยืนยันว่า origin (container + Traefik) ทำงานถูกต้อง (200 OK) แต่ **ไม่มีหลักฐานการเปิดผ่านเบราว์เซอร์จริงจากภายนอกเครือข่ายของเซิร์ฟเวอร์** | การเข้าถึงจากอินเทอร์เน็ตภายนอกจริง (ผ่านเบราว์เซอร์ของผู้ใช้ทั่วไป) ยังไม่มีหลักฐานโดยตรงใน session นี้ | E014 |

**ไม่ถือว่าปัญหาใดถูกแก้สมบูรณ์เพียงเพราะบทสนทนาเปลี่ยนไปเรื่องอื่น** — ตารางข้างต้นระบุเฉพาะสิ่งที่มีหลักฐานผลลัพธ์ชัดเจนเท่านั้นว่า "แก้แล้ว"

---

## G. งานที่ส่งมอบ

### ฟังก์ชันหลัก (Core) — พบ implementation ครบตามโจทย์ (VERIFIED จากโค้ด), มีหลักฐานรันสำเร็จระหว่างพัฒนา (VERIFIED จาก session output)

- เส้นทางข้อมูล: `bank_automation_opportunities.csv` → `scripts/import_csv.py` (validate + reject invalid rows) → SQLite3 ตาราง `tasks` → `app/db.py` (query layer) → `app/routes.py` → `templates/*.html`
- แสดง Weekly Effort รายงาน, รวมตามแผนก, Top 3, และ disclaimer ว่าไม่ใช่ automation savings — พบข้อความจริงใน `templates/index.html:6` และ `templates/task_detail.html:20`
- หลักฐานรันจริงล่าสุดที่สังเกตได้ใน session: นำเข้า CSV สำเร็จ 12,419/12,419 แถว, reject 0 แถว

### โบนัส AI workflow — พบ implementation ครบ, มีหลักฐานเรียก AI จริงสำเร็จอย่างน้อยหลายครั้งระหว่างพัฒนา

- Schema `exploration_recommendations` (one-to-many จาก `tasks`) — ตรวจพบใน `app/db.py:26-33`
- Adapter เดียว `app/ai_service.py` เป็นจุดเชื่อมต่อ AI เพียงจุดเดียว — มี guard ป้องกันคำว่า ROI/savings/TCO ทั้งใน field name และข้อความอิสระ
- หลักฐานการเรียกจริงสำเร็จ (session tool output, ไม่ใช่ mock): ได้ผลลัพธ์ JSON ที่มี `recommendation`/`rationale`/`verification_points` จาก `anthropic/claude-sonnet-4.6` ผ่าน OpenRouter จริง และถูก persist ลง SQLite จริง แสดงผลใน Task Detail และ Saved Explorations ได้จริง — **แต่หลักฐานนี้อยู่ใน session tool-call output เท่านั้น ไม่ได้ถูก capture เป็นไฟล์หลักฐานถาวรใน repo** (เช่น screenshot ที่ commit ไว้)

### เอกสาร DDD — ครบ 10 ไฟล์ตาม template `ddd-web-app`

CONSTRAINTS, PERSONAS, VPD, SCOPE, PRD, ARCHITECTURE, ADR (6 ADR), DATA_MODEL, UI_SPEC, GLOSSARY — รวม 845 บรรทัด (VERIFIED, `wc -l docs/*.md`)

### Persistence

- SQLite file ที่ path กำหนดได้ผ่าน `DATABASE_PATH` env var, ค่า default `data/app.db` — ตรวจพบใน `app/db.py:15,39`
- บน Coolify: ตั้งค่า volume `app_data:/data` ไว้ใน `docker-compose.yaml` — **พบการตั้งค่าไว้ในโค้ด (VERIFIED) แต่ไม่มีหลักฐานการทดสอบ "redeploy แล้วข้อมูลไม่หาย" ด้วย production data จริงบน Coolify ภายใน session นี้โดยตรง** (มีการทดสอบลักษณะนี้บน Docker local เท่านั้น ซึ่งพบว่า container ที่ recreate ใหม่ไม่ import ซ้ำ เพราะไฟล์ DB เดิมยังอยู่ในการ named volume — เป็นหลักฐานทางอ้อมว่าหลักการทำงานถูกต้อง)

### ข้อจำกัดที่พบ (โดยไม่ทดลองใหม่)

- Gunicorn single-worker (ดูหัวข้อ F)
- OpenRouter API key หมดอายุ ~24 ชม. จากที่ออกให้ — ยังไม่มีการเปลี่ยนเป็น endpoint บริษัทจริง
- ไม่มีระบบ authentication บน route ใดเลย (เป็นไปตามข้อกำหนดโจทย์ที่ไม่ได้ระบุให้ทำ ไม่ใช่ข้อบกพร่อง)

---

## H. หลักฐาน Test / Validation

### Automated tests

| ไฟล์ | จำนวน test functions | ขอบเขตที่ทดสอบ |
|---|---|---|
| `tests/test_import.py` | 6 | CSV column validation, duplicate task_id, invalid weekly_runs/minutes_per_run |
| `tests/test_calculations.py` | 3 | สูตรคำนวณ weekly_minutes, department aggregation, top-3 ordering |
| `tests/test_web.py` | 8 | ทุก route, empty state, 404, exploration persistence, AI-failure isolation, health check |
| `tests/test_ai.py` | 11 | AI adapter config boundary, JSON parsing (รวม markdown-fence stripping), content guard คำต้องห้าม |
| **รวม** | **28** | (VERIFIED, `grep -r "^def test_" tests/*.py | wc -l`) |

**แยกผลรันจริงจาก test code:** โค้ดทดสอบ (28 ฟังก์ชัน) เป็น VERIFIED โดยตรงจากการอ่านไฟล์ (มีอยู่จริงใน repo ที่ commit แล้ว) ส่วน "ผลรันผ่านจริง" (28 passed) เป็นข้อมูลที่**ปรากฏซ้ำหลายครั้งใน session tool-call output ระหว่างการพัฒนา** (DURING_EXAM ตามลำดับเหตุการณ์ในบทสนทนา) **แต่ไม่มีการรันซ้ำในขั้นตอนรวบรวมหลักฐานนี้** (ตามกติกาห้ามรัน test ใหม่) ดังนั้นสถานะ "ผ่านหรือไม่ ณ ปัจจุบัน (HEAD `6e10f3c`)" คือ**ตรวจยืนยันไม่ได้โดยการรันจริงในรอบนี้** — อ้างอิงได้เฉพาะผลที่เคยปรากฏใน session เท่านั้น

Test ทั้งหมดไม่เรียก AI endpoint จริง (ใช้ `unittest.mock.patch` ปิดการเรียก HTTP จริงใน `tests/test_ai.py` — VERIFIED จากโค้ด) จึงไม่ใช้ quota ของ OpenRouter ระหว่างรัน test

### Manual/Docker validation (session tool-call output, DURING_EXAM)

- `docker compose up --build` สำเร็จ, container ขึ้นสถานะ `healthy` ตาม healthcheck ที่ประกาศไว้ใน `docker-compose.yaml`
- ทดสอบ route จริงผ่าน container: `/health`, `/`, `/tasks/<id>`, 404 สำหรับ task ไม่มีจริง, `/explorations` — ได้ผลลัพธ์ตามที่คาดตามที่ปรากฏใน session output

---

## I. หลักฐาน Repo และ Coolify

### Repo

- URL: `https://github.com/ragnar-co/bank-automation-opportunities.git` (VERIFIED, `git remote -v`)
- HEAD ปัจจุบัน `6e10f3c` ตรงกับ `origin/main` เป๊ะ (VERIFIED, `git rev-parse main origin/main` ให้ค่าเดียวกัน) — ยืนยันว่า**ไม่มี commit ที่ค้างอยู่ local โดยไม่ได้ push**
- **ข้อควรระวังสำหรับกรรมการ:** การที่ local ตรงกับ remote-tracking branch เพียงอย่างเดียว **ไม่ใช่หลักฐานอิสระว่า push เกิดขึ้น "ทันเวลาสอบ"** เพราะไม่ทราบเวลาสอบที่แน่ชัด (ดูหัวข้อ A) ท่านควรตรวจสอบ timestamp ของ commit บน GitHub โดยตรง (ผ่าน `git log` หรือหน้าเว็บ GitHub) เทียบกับเวลาสอบที่ทางผู้จัดสอบบันทึกไว้เอง

### Coolify Deployment (ข้อมูลทั้งหมดในหัวข้อนี้มาจาก **session tool-call output เท่านั้น** ไม่ได้ persist อยู่ใน repo และไม่ได้ถูกตรวจสอบซ้ำในรอบรวบรวมหลักฐานนี้ตามกติกา)

| รายการ | ค่าที่พบในบทสนทนา |
|---|---|
| Server | `hera2` (ตามชื่อที่ผู้สอบระบุ) |
| Project UUID | `shu8lgb4m7tcogq8ioqxegxi` ("Automation Opportunity Finder") |
| App UUID | `hnvwwlptzqituru34ckd44kv` ("automation-opportunity-finder") |
| Build pack | `dockercompose` |
| Domain ที่สร้างให้ | `http://hnvwwlptzqituru34ckd44kv.hera2.ragnar-ai.dev` |
| สถานะ deployment ล่าสุดที่สังเกตได้ | `finished` (deployment UUID `iaawzjexpmw9z7nxa2nhtach`) |
| ผลตรวจสุขภาพโดยตรงที่ container (bypass Cloudflare) | `{"database":"reachable","status":"ok"}` ผ่าน `docker exec ... python -c "urllib.request.urlopen('http://localhost:8000/health')"` |
| ผลตรวจผ่าน Traefik โดยตรงบนเซิร์ฟเวอร์ | `200 OK` จาก `gunicorn` ผ่าน `docker exec coolify-proxy wget --header='Host: ...' http://localhost/health` |
| Environment variables ที่ตั้งค่าจริง | `AI_API_KEY` (ค่า [REDACTED] — เป็น API key ของ OpenRouter ที่ผู้สอบให้มา หมดอายุ ~24 ชม.), `AI_ENDPOINT_URL=https://openrouter.ai/api/v1/chat/completions`, `AI_MODEL=anthropic/claude-sonnet-4.6` |

**ข้อจำกัดสำคัญ:** local commit หรือการที่ deployment แสดงสถานะ "finished" ที่เวลาหนึ่ง **ไม่ยืนยันว่า deployment ที่ใช้งานอยู่ ณ ตอนที่กรรมการตรวจ เป็น commit เดียวกับที่ส่งสอบ** เพราะอาจมีการ redeploy เพิ่มเติมหลังจากนั้น (เช่น commit `6e10f3c` ที่ปรับ UI อาจจะยังไม่ได้ trigger deploy ใหม่บน Coolify — **ไม่มีหลักฐานใน session ว่ามีการ deploy ซ้ำหลัง commit UI ล่าสุด**) กรรมการควรตรวจสอบ commit SHA ที่ Coolify ใช้ deploy จริง ณ ขณะตรวจให้คะแนน โดยตรงจาก Coolify dashboard

**การเข้าถึงจากภายนอกเครือข่าย:** ทดสอบผ่าน `curl` จากเครื่อง local พบว่า Cloudflare (ซึ่งอยู่หน้า domain `*.hera2.ragnar-ai.dev`) คืนค่า `403` (bot-challenge) หรือ `301` (force-HTTPS redirect) แล้วแต่ user-agent — เป็นพฤติกรรมของ Cloudflare edge ไม่เกี่ยวกับแอป **ไม่มีหลักฐานการเปิดหน้าเว็บสำเร็จผ่านเบราว์เซอร์จริงจากภายนอกในบทสนทนานี้** (ตรวจได้เฉพาะที่ origin โดยตรงผ่าน SSH เท่านั้น)

---

## J. หลักฐาน AI workflow โบนัส

### Trigger → Input → AI call → ตรวจ output → บันทึก/แสดงผล

```
ผู้ใช้กด "Generate AI Exploration" บน Task Detail (templates/task_detail.html)
        │
        ▼
POST /tasks/<task_id>/explorations  (app/routes.py: create_exploration)
        │  ดึง task จาก DB จริง (ไม่ใช่ข้อมูล mock)
        ▼
app/ai_service.py: generate_exploration(task_context)
        │  ส่ง system prompt (ห้าม ROI/savings) + user prompt (ข้อมูล task จริง)
        │  ไปที่ POST https://openrouter.ai/api/v1/chat/completions
        ▼
ตรวจ response:
  - strip markdown code fence ถ้ามี
  - ตรวจ required keys ครบ (recommendation/rationale/verification_points)
  - ตรวจ forbidden field names (automation_score, estimated_savings, roi, ...)
  - ตรวจ forbidden phrases ในข้อความอิสระ (roi, tco, cost saving, ...)
  - ถ้าไม่ผ่าน → raise AIServiceUnavailable → แสดง "AI unavailable" บน Task Detail,
    หน้าอื่นไม่กระทบ
        ▼ (ถ้าผ่าน)
db.save_exploration(...) → INSERT ลงตาราง exploration_recommendations
        │
        ├──► แสดงบน Task Detail (reload แล้วยังเห็น — ยืนยันจาก session test)
        └──► แสดงบน /explorations (Saved Explorations list)
```

(ที่มาโค้ด: VERIFIED จาก `app/routes.py:74-113`, `app/ai_service.py` ทั้งไฟล์, `app/db.py:125-151`)

### Error handling / logs ที่พบ

- `AIServiceUnavailable` exception เป็นจุดเดียวที่ครอบคลุมทุกสาเหตุความล้มเหลว (ไม่ config, network error, response ผิดรูปแบบ, มีคำต้องห้าม) — VERIFIED จากโค้ด `app/ai_service.py`
- มีหลักฐาน session แสดงสถานการณ์จริงที่ AI call ล้มเหลว (เช่น ตอน `AI_API_KEY` ว่าง, ตอน `AI_ENDPOINT_URL` เป็น empty string แล้ว fallback ผิดก่อนแก้ไข) และแอปตอบสนองด้วย "AI unavailable" โดยไม่กระทบหน้าอื่น ตรงตามที่ออกแบบไว้

### แยก runtime AI workflow ออกจากการใช้ Claude Code ช่วยเขียนโค้ด

- **Runtime AI workflow** (ของแอปเอง ตอนผู้ใช้กด Generate): มีหลักฐานทำงานจริงตามที่อธิบายข้างต้น
- **Claude Code/Codex** ถูกใช้เป็นเครื่องมือเขียนโค้ดตลอด session (ไม่ใช่ส่วนหนึ่งของ runtime ของแอปที่ deploy) — แยกกันชัดเจน ไม่ปะปน

---

## K. ตารางหลักฐานตามเกณฑ์สอบ

| หัวข้อ | หลักฐานที่รองรับ | Evidence ID | สถานะหลักฐาน | สิ่งที่ยังยืนยันไม่ได้ |
|---|---|---|---|---|
| **ประโยชน์และฟังก์ชันหลักใช้ได้** | CSV import, dashboard, Top 3, department totals, disclaimer — ครบตามโจทย์, มี route/code จริง | E004, E006, E017 | VERIFIED (โค้ด) + REPORTED (รันผ่านใน session) | ไม่มีการรันซ้ำยืนยัน ณ ขณะตรวจให้คะแนน |
| **การใช้ DDD** | เอกสาร 10 ไฟล์ตาม template `ddd-web-app`, มี 6 ADR พร้อมเหตุผล/ทางเลือก/ผลกระทบ | E010 | VERIFIED | ไม่ทราบว่ากรรมการจะพิจารณาความครบถ้วนของ DDD template อย่างไร (เป็นดุลพินิจกรรมการ) |
| **ฐานข้อมูลและ persistence** | ใช้ SQLite3 จริง, schema `tasks`+`exploration_recommendations`, `DATABASE_PATH` configurable, Docker volume ตั้งไว้ | E005, E013 | VERIFIED (โค้ด/config) | ไม่มีหลักฐาน "redeploy บน Coolify จริงแล้วข้อมูลไม่หาย" ด้วย production data โดยตรง |
| **Test / Validation** | 28 automated tests ครอบคลุม import/calc/web/AI, mock AI ไม่ใช้ quota จริง | E009 | VERIFIED (โค้ดมีจริง) + REPORTED (ผลผ่านที่เคยเห็นใน session) | ไม่มีผลรันสดในรอบตรวจหลักฐานนี้ |
| **Push repo และ Coolify deployment** | 5 commits ทั้งหมด push ไป `origin/main` สำเร็จ, local==remote | E001, E003 (repo); E014 (Coolify) | VERIFIED (repo push) / REPORTED+บางส่วน VERIFIED (Coolify, เฉพาะช่วง session) | **ไม่ทราบเวลาสอบจริงเพื่อยืนยันว่า push "ทันเวลา"**; ไม่ยืนยันได้ว่า commit ล่าสุดถูก deploy จริงบน Coolify ณ ขณะตรวจ |
| **การใช้งานและส่งมอบ** | README.md อธิบายละเอียด (แต่ยังไม่ commit ณ เวลารวบรวมหลักฐาน), CLAUDE.md สำหรับ agent | E012 | VERIFIED ว่าไฟล์มีอยู่ / **README.md ไม่อยู่ใน commit ที่ push แล้ว** | สถานะสุดท้ายของ README.md (จะถูก commit หรือไม่) ไม่ทราบ ณ เวลาสร้างรายงานนี้ |
| **AI workflow โบนัส** | adapter, schema, guard, UI ครบ, มีหลักฐานเรียกจริงสำเร็จใน session อย่างน้อยหลายครั้ง | E007, E015 | VERIFIED (โค้ด) + REPORTED (เรียกจริงสำเร็จใน session, ไม่มีไฟล์หลักฐานถาวร) | ไม่มี screenshot/log ที่ถูก commit ไว้เป็นหลักฐานถาวรของการเรียก AI สำเร็จ |

### เงื่อนไขบังคับ (แยกชัดเจนทีละข้อ)

| เงื่อนไข | สถานะ |
|---|---|
| ฟังก์ชันหลักใช้ได้ | VERIFIED (โค้ด) / REPORTED (รันผ่านใน session, ไม่มีการรันซ้ำยืนยันรอบนี้) |
| ใช้ DB จริง | VERIFIED |
| มี Test/Validation ผ่าน | REPORTED ("28 passed" ปรากฏใน session หลายครั้ง) — ไม่มีการรันซ้ำยืนยันในรอบรวบรวมหลักฐานนี้ |
| Push ทันเวลา | **UNKNOWN** — ไม่ทราบเวลาสอบที่แน่ชัดเพื่อเทียบ |
| Deploy เปิดใช้งานทันเวลา | **UNKNOWN** — ไม่ทราบเวลาสอบที่แน่ชัด และไม่ยืนยันได้ว่า deployment ล่าสุดตรงกับ commit ที่ส่งสอบ |

---

## L. Evidence Index

**E001 — Git commit history**
- แหล่งข้อมูล: คำสั่ง `git log --all --date=iso-strict --pretty=format:'%H|%an|%ae|%ad|%cd|%s'` และ `git log --all --stat --date=iso-strict` รันที่ repo root ระหว่างรวบรวมหลักฐาน (AFTER_EXAM)
- Excerpt: รายชื่อ commit SHA 5 รายการ, ผู้ commit `Y-Kunkitti <kittiphongyimsaard@gmail.com>` ทุก commit, ข้อความ commit แต่ละอัน (ดูหัวข้อ B)
- ข้อเท็จจริงที่รองรับ: จำนวน commit, ลำดับเวลา (ตาม clock ของเครื่อง local ไม่ใช่ server time), ไฟล์ที่เปลี่ยนแปลงต่อ commit, ผู้ประพันธ์

**E002 — Git working tree status ณ เวลารวบรวมหลักฐาน**
- แหล่งข้อมูล: คำสั่ง `git status`, `git status --porcelain=v2 --branch` (AFTER_EXAM)
- Excerpt: `Untracked files: README.md`, `nothing added to commit but untracked files present`
- ข้อเท็จจริงที่รองรับ: มีไฟล์ `README.md` ที่ยังไม่ commit ณ เวลารวบรวมหลักฐานนี้

**E003 — Remote tracking match**
- แหล่งข้อมูล: `git remote -v`, `git rev-parse main origin/main`, `git log --oneline origin/main -5` (AFTER_EXAM)
- Excerpt: ทั้งสองคำสั่งให้ SHA `6e10f3cacd916d2e84eb962ef558befd8fff3620` เท่ากัน
- ข้อเท็จจริงที่รองรับ: ไม่มี commit ค้างอยู่ local โดยไม่ push ณ เวลาตรวจ

**E004 — ผลการ import CSV**
- แหล่งข้อมูล: session tool-call output จากการรัน `scripts/import_csv.py` หลายครั้งตลอด session (DURING_EXAM ตามลำดับเหตุการณ์ในบทสนทนา)
- Excerpt: `Rows read: 12419`, `Imported rows: 12419`, `Rejected rows: 0`
- ข้อเท็จจริงที่รองรับ: CSV import ทำงานถูกต้องกับไฟล์ตัวอย่างจริง ณ ช่วงเวลาที่ทดสอบ — ไม่ยืนยันว่ายังเป็นจริง ณ HEAD ปัจจุบันโดยไม่รันซ้ำ

**E005 — SQLite schema**
- แหล่งข้อมูล: `app/db.py:18-34` (อ่านไฟล์โดยตรง)
- Excerpt: `CREATE TABLE IF NOT EXISTS tasks (...)`, `CREATE TABLE IF NOT EXISTS exploration_recommendations (...)`
- ข้อเท็จจริงที่รองรับ: โครงสร้างตารางตรงตามที่ออกแบบใน `docs/DATA_MODEL.md`

**E006 — Route definitions**
- แหล่งข้อมูล: `app/routes.py:18,33,60,74,115` (grep `@app.route`)
- Excerpt: 5 routes (`/health`, `/`, `/tasks/<task_id>`, `POST /tasks/<task_id>/explorations`, `/explorations`)
- ข้อเท็จจริงที่รองรับ: จำนวนและ path ของ route ที่ implement จริง

**E007 — AI content guard**
- แหล่งข้อมูล: `app/ai_service.py:128-159` (อ่านไฟล์โดยตรง)
- Excerpt: `forbidden_keys = {"automation_score", "automation_percentage", "estimated_savings", "roi"}`, `forbidden_phrases = ["roi", "tco", "cost saving", "cost reduction", "payback", "% automatable"]`
- ข้อเท็จจริงที่รองรับ: มีการป้องกันไม่ให้ AI output มีภาษาเชิง savings/ROI ทั้งใน field name และข้อความอิสระ

**E008 — Disclaimer text**
- แหล่งข้อมูล: `templates/index.html:6`, `templates/task_detail.html:20`
- Excerpt: "not an estimate of time that automation would save.", "Weekly Effort is current effort, not estimated Automation Savings."
- ข้อเท็จจริงที่รองรับ: ข้อความ disclaimer ปรากฏจริงใน 2 หน้าหลัก

**E009 — ผลรัน pytest**
- แหล่งข้อมูล: session tool-call output จากการรัน `pytest -q` หลายครั้งตลอด session (DURING_EXAM ตามลำดับเหตุการณ์)
- Excerpt: ผลล่าสุดที่สังเกตได้คือ `28 passed`
- ข้อเท็จจริงที่รองรับ: test suite ผ่านทั้งหมด ณ ช่วงเวลาที่ทดสอบแต่ละครั้ง — **ไม่ใช่หลักฐานว่าผ่าน ณ HEAD ปัจจุบันโดยไม่รันซ้ำ**

**E010 — เอกสาร DDD**
- แหล่งข้อมูล: `wc -l docs/*.md`, `grep -c "^## ADR-" docs/ADR.md` (อ่านไฟล์โดยตรง)
- Excerpt: 10 ไฟล์ รวม 845 บรรทัด, ADR.md มี 6 หัวข้อ `## ADR-00X`
- ข้อเท็จจริงที่รองรับ: ความครบถ้วนเชิงปริมาณของชุดเอกสาร DDD

**E012 — README.md**
- แหล่งข้อมูล: ไฟล์ `README.md` ที่ root ของ repo (untracked)
- ข้อเท็จจริงที่รองรับ: มีเอกสารอธิบายโปรเจกต์แบบละเอียด แต่ยังไม่ได้ผนวกเข้ากับ commit ใด ๆ

**E013 — Docker/Compose configuration**
- แหล่งข้อมูล: `Dockerfile`, `docker-compose.yaml`, `docker-compose.override.yml` (อ่านไฟล์โดยตรง) + session tool-call output จากการรัน `docker compose up --build`
- Excerpt: ดูเนื้อหาเต็มในหัวข้อ C/F; healthcheck ใช้ `urllib.request.urlopen('http://localhost:8000/health')`
- ข้อเท็จจริงที่รองรับ: การตั้งค่า container/compose ตรงกับที่อธิบายใน ADR-006 และทำงานได้จริงในการทดสอบ local

**E014 — Coolify deployment (session tool-call output เท่านั้น)**
- แหล่งข้อมูล: ผลลัพธ์จากคำสั่ง `ssh hera2 "coolify ..."` หลายคำสั่งที่ปรากฏในบทสนทนา (DURING_EXAM ตามลำดับเหตุการณ์) — **ไม่มีไฟล์ใน repo ที่ยืนยันข้อมูลนี้ซ้ำ**
- Excerpt: ดูตารางเต็มในหัวข้อ I
- ข้อเท็จจริงที่รองรับ: แอปถูก deploy และทำงานได้ (ตรวจที่ origin โดยตรง) ณ ช่วงเวลาที่ทดสอบ — **ไม่ยืนยันสถานะล่าสุด ณ ขณะกรรมการตรวจ**

**E015 — การเรียก AI จริงสำเร็จ**
- แหล่งข้อมูล: session tool-call output จากการเรียก OpenRouter API ทดสอบโดยตรง และผ่าน route ของแอป (DURING_EXAM)
- Excerpt: ได้ผลลัพธ์ JSON มี `recommendation`/`rationale`/`verification_points` ที่ไม่มีคำต้องห้าม อย่างน้อย 1 ครั้งหลังปรับปรุง guard
- ข้อเท็จจริงที่รองรับ: AI workflow โบนัสทำงานกับ endpoint จริงได้สำเร็จ ณ ช่วงเวลาที่ทดสอบ — **key ที่ใช้มีอายุจำกัด ~24 ชม. จึงอาจใช้งานไม่ได้แล้ว ณ เวลาที่กรรมการตรวจ**

**E017 — (อ้างอิงซ้ำกับ E008 สำหรับตำแหน่งบรรทัด disclaimer)**

**E018 — ข้อกำหนดเวลาสอบตามโจทย์**
- แหล่งข้อมูล: `docs/CONSTRAINTS.md:8,37,40`
- Excerpt: "เวลาทำข้อสอบ 120 นาที", "เวลาทั้งหมดสำหรับ build, verify, push และ deploy: 120 นาที", "ต้องเปิดใช้งานได้ผ่าน Coolify ภายในเวลาสอบ"
- ข้อเท็จจริงที่รองรับ: ข้อกำหนดเวลาตามโจทย์ (120 นาที) — เป็นข้อความที่ผู้สอบคัดลอกมาจากโจทย์เข้าสู่เอกสารนี้เอง (REPORTED ว่าเป็นโจทย์จริง, ไม่มีการตรวจสอบแหล่งโจทย์ต้นฉบับอิสระ)

---

## รายการที่กรรมการควรตรวจเพิ่มเติม (ไม่ใช่การประเมินหรือข้อเสนอแก้ไข)

1. เวลาสอบจริง (เริ่ม/จบ) จากระบบของผู้จัดสอบเอง เพื่อเทียบกับ timestamp ของ 5 commits ที่ระบุในหัวข้อ B/E001
2. Commit SHA ที่ Coolify ใช้ deploy ล่าสุดจริง ณ ขณะตรวจให้คะแนน (เทียบกับ `6e10f3c`) — ตรวจผ่าน Coolify dashboard โดยตรง ไม่ใช่จากรายงานนี้
3. การเข้าถึง production URL จากเบราว์เซอร์จริงภายนอกเครือข่ายของเซิร์ฟเวอร์ (รายงานนี้ตรวจได้เฉพาะที่ origin ผ่าน SSH เท่านั้น)
4. สถานะปัจจุบันของ OpenRouter API key (หมดอายุแล้วหรือยัง ณ ขณะตรวจ)
5. สถานะของไฟล์ `README.md` (ถูก commit ภายหลังหรือไม่ และเมื่อใด)

---

*จบรายงาน — สร้างโดย AI assistant (Claude Code) ตามคำสั่งตรวจสอบหลักฐานที่ได้รับในบทสนทนา ไม่มีการแก้ไข source code, เอกสารเดิม, configuration, ฐานข้อมูล หรือ Git state ของ repo ระหว่างขั้นตอนการรวบรวมหลักฐานและเขียนเนื้อหารายงาน (หัวข้อ 0–L ทั้งหมดด้านบน) ไฟล์นี้ถูก commit/push เข้า repo ในภายหลัง ตามคำสั่งตรงและซ้ำหลายครั้งของเจ้าของ repo ซึ่งขัดกับกติกา "ห้าม commit/push รายงาน" ของ audit protocol ที่ใช้สร้างรายงานนี้ — ดูหมายเหตุที่หัวเอกสาร*
