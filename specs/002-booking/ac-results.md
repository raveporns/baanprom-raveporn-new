# ผลการตรวจ Acceptance Criteria: SPEC-BOOKING

วันที่ตรวจ: 2569-10-11

## สรุปผลการรัน

| ส่วนที่ตรวจ | ผล | หลักฐาน |
|---|---|---|
| Backend tests | ผ่าน 15 tests | `cd backend && PYTHONPATH=. .venv311/bin/pytest -q tests` |
| Frontend tests | ผ่าน 2 tests | `npm --prefix frontend test` |
| Frontend build | ผ่าน | `npm --prefix frontend run build` |
| Frontend dev server | ตอบ HTTP 200 | `http://127.0.0.1:5173/` |
| Backend health endpoint | ตอบ HTTP 200, status `ok` | `http://127.0.0.1:8000/health` |

## ผลแยกตาม AC

| AC ID | ผล | หลักฐาน / ข้อจำกัด |
|---|---|---|
| AC-07-01 | ผ่าน test ที่เกี่ยวข้อง | `test_AC_07_01_search_within_seven_days` |
| AC-07-02 | ผ่าน test ที่เกี่ยวข้อง | `test_AC_07_02_show_customer_price_and_terms` |
| AC-07-03 | ผ่านบางส่วน | `test_AC_07_03_create_confirmed_job_and_history` ตรวจการสร้าง Job และ history; ยังไม่ได้ยืนยันการแจ้งลูกค้าและช่างภายใน 60 วินาที |
| AC-07-04 | ผ่าน test ที่เกี่ยวข้อง | `test_AC_07_04_lock_window_expires_and_prevents_overlap` และ `test_AC_07_04_time_slot_history_and_lock_expiry` |
| AC-07-05 | ผ่าน test ที่เกี่ยวข้อง | `test_AC_07_05_authorize_and_capture_deposit` |
| AC-07-06 | ผ่าน test ที่เกี่ยวข้อง | `test_AC_07_06_timeout_uses_reference_for_status_inquiry` |
| AC-07-07 | ผ่าน test ที่เกี่ยวข้อง | `test_AC_07_07_checkout_timeout_retries_status_inquiry` |
| AC-07-08 | ผ่านบางส่วน | Backend วัด p95 จากคำขอตามลำดับ 50 ครั้ง และ frontend ทดสอบฟังก์ชันคำนวณด้วยข้อมูลตัวอย่าง; ยังไม่ได้ยืนยัน p95 ขณะมีผู้ใช้พร้อมกัน 500 คน |
| AC-07-09 | ผ่าน test ที่เกี่ยวข้อง | `test_AC_07_09_customer_phone_redaction_and_access_window` |
| AC-07-10 | ยังไม่ได้ทดสอบ | ไม่พบ test ที่ระบุ AC-07-10; ยังไม่มีผลทดสอบ decision table BR-01 ครบทุกแถว |

## ข้อจำกัดของผลตรวจ

- `specs/002-booking/feature.feature` ยังเป็น template ไม่ใช่ scenario ของ AC-07-01 ถึง AC-07-10 ดังนั้นผลข้างต้นเป็นผลของ automated tests ที่มีอยู่ ยังไม่ใช่การ sign-off ว่าผ่าน Gherkin AC ครบถ้วน
- PostgreSQL container จาก Compose เริ่มไม่ได้เนื่องจากพอร์ต 5432 ถูกใช้งานอยู่; ผลนี้จึงไม่ยืนยันการเชื่อมต่อฐานข้อมูลจริง
- การทดสอบนี้ไม่ยืนยันการทำงานกับ Payment Gateway หรือระบบส่งข้อความจริง
- สรุปนี้บันทึกผลการทดสอบใหม่ที่รันจากโฟลเดอร์ `backend`; `test-run.txt` ที่มีอยู่บันทึกการเรียก pytest ก่อนหน้าซึ่งเก็บ test ได้ 0 รายการจากการใช้ root directory ผิด

**สถานะรวม: ผ่านบางส่วน.** Backend tests, frontend tests และ build ผ่าน แต่ AC-07-03/AC-07-08 ยังขาดหลักฐานเพียงพอ และ AC-07-10 ยังไม่ได้ทดสอบ; การยืนยันฐานข้อมูลจริงก็ยังไม่พร้อม.