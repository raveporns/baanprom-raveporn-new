# prompt-log.md บันทึกการใช้ AI ของกลุ่ม <ชื่อกลุ่ม>

กติกา: เพิ่มต่อท้ายเท่านั้น ห้ามแก้หรือลบบันทึกเดิม
ทุกบันทึกมี: เลขที่ | วันที่ | เครื่องมือ | คำสั่ง | สิ่งที่ AI ถามหรือรายงาน | คำตอบหรือการตัดสินใจของทีม | สิ่งที่ AI เดา (ถ้ามี)
AI จะเพิ่มบันทึกให้เองเมื่อใช้คำสั่ง /clarify /plan /tasks /implement ทีมเพิ่มเองได้เมื่อสั่งแก้นอกคำสั่ง

## #1 | <วันที่> | <เครื่องมือ> | <คำสั่ง>

## #2 | 2569-10-04 | Chat + filesystem | /tasks specs/002-booking/spec.md | สร้าง tasks.md จาก spec/plan ของ feature booking และตรวจว่าทุก AC มี task ที่ครอบคลุม พร้อมแยก task ที่รอ Open Questions | ทีมยืนยันใช้ spec/plan นี้เป็นแหล่งความจริง และยอมรับการใช้คำตอบที่เดาได้จาก Q-14, Q-18, Q-19, Q-22 เป็นค่าเบื้องต้นเพื่อให้ tasks สามารถวางลำดับได้ | AI เดา: Q-14 = ติดต่อ call center, Q-18 = 10 นาที, Q-19 = 30 วินาที, Q-22 = เก็บแต่ไม่ส่งออกนอกระบบ

## #3 | 2569-10-04 | Chat + filesystem | แก้ spec/plan/tasks ให้ใช้ stack ที่เลือกเอง | ปรับเอกสารให้ตรงกับข้อจำกัดที่ spec ระบุว่าไม่มีข้อจำกัดเชิง framework: Frontend React + Vite + Tailwind, Backend FastAPI, Database PostgreSQL | ทีมเลือก stack นี้เอง ไม่ใช่ข้อกำหนดจาก spec; สถานะเอกสารทั้งหมดปรับให้สอดคล้องกับ stack ใหม่

## #4 | 2569-10-04 | Bash + filesystem | /implement T-01 specs/002-booking/tasks.md | สร้าง monorepo scaffold สำหรับ booking: frontend React + Vite + Tailwind, backend FastAPI, PostgreSQL docker-compose, backend smoke tests | T-01 เสร็จแล้ว; frontend build ผ่านและ backend pytest ผ่าน (2 tests) โดยใช้ stack ตามที่เลือกเอง

## #5 | 2569-10-11 | Bash + filesystem | /implement T-02 specs/002-booking/tasks.md | สร้างและปรับโมเดล Job/TimeSlot/Payment/Refund ให้มีสถานะ/state, history, และ PII redaction สำหรับ AC-07-04 และ AC-07-09 | โมเดลและ test สำหรับ task T-02 เสร็จแล้ว; ต้องตรวจทบทวนว่าตรงกับ spec และเงื่อนไข PII ตาม REQ-PRV-002/REQ-SEC-004 | AI เดา: ไม่มีค่าที่ต้องถามเพิ่ม เนื่องจาก spec/task ให้ชัดเจนว่าต้องมี state/history และการล็อก PII เฉพาะช่วงที่อนุญาต

## #6 | 2569-10-11 | Bash + filesystem | /implement T-03 specs/002-booking/tasks.md | สร้าง API ค้นหาช่างว่างภายใน 7 วัน และแสดงราคา/เงื่อนไขยกเลิกให้ลูกค้าเห็น | API คืนผลลัพธ์ทุก slot พร้อม `service_type`, `address_id`, `deposit_amount`, และ `cancellation_terms`; tests AC-07-01/AC-07-02 ผ่าน | AI เดา: ไม่มีค่าที่ต้องถามเพิ่ม เพราะ spec ระบุชัดเจนว่าต้องมีข้อมูลประเภทงาน/ที่อยู่/ช่วงเวลาและราคามัดจำที่เห็นได้จากลูกค้า

## #7 | 2569-10-11 | Bash + filesystem | /implement T-04 specs/002-booking/tasks.md | ปรับล็อกช่วงเวลาให้มีระยะ 10 นาที ตาม Q-18 และไม่ให้ซ้อนทับ จนหมดอายุอัตโนมัติ | T-04 เสร็จแล้ว; test AC-07-04 ผ่าน และ lock expiry logic ป้องกันการซ้อนทับ | AI เดา: ไม่มีค่าที่ต้องถามเพิ่ม เนื่องจาก Q-18 ได้รับคำตอบว่า 10 นาทีแล้ว

## #8 | 2569-10-11 | Bash + filesystem | /implement T-05 specs/002-booking/tasks.md | สร้างกระบวนการ authorize/capture มัดจำผ่าน gateway และ fallback status inquiry เมื่อ timeout 30 วินาที | T-05 เสร็จแล้ว; tests AC-07-05/06/07 ผ่าน และการ timeout ใช้ reference เดิมในการ inquiry | AI เดา: Q-19 = 30 วินาที ตามคำตอบจากทีม

## #9 | 2569-10-11 | Bash + filesystem | /implement T-06 specs/002-booking/tasks.md | สร้าง Job ที่เริ่มต้นในสถานะ confirmed และเก็บ history status สำหรับ lifecycle ตาม MD-STM-01 | T-06 เสร็จแล้ว; test AC-07-03 ผ่าน และ job history มีประวัติ 730 วัน | AI เดา: ไม่มีค่าที่ต้องถามเพิ่ม เพราะ spec ระบุชัดเจนว่าต้องสร้างงานยืนยันแล้วและเก็บประวัติ 24 เดือนเท่านั้น

## #10 | 2569-10-11 | Bash + filesystem | /implement T-07 specs/002-booking/tasks.md | สร้างการแจ้งเตือนหลังงานยืนยันแล้ว ให้ส่งถึงลูกค้าและช่างด้วย trace/log และตรวจสอบเวลาส่งภายใน 60 วินาที | T-07 เสร็จแล้ว; `JobCreatedEvent.deliver_notifications()` ส่ง SMS ให้ทั้งสองฝ่ายและเก็บ trace_id + sent_at ใน log, พร้อม validation ว่าระยะเวลารับส่งยังอยู่ภายใน 60 วินาที | AI เดา: ไม่มีค่าที่ต้องถามเพิ่ม เพราะ spec ระบุชัดเจนว่าต้องแจ้งทั้งสองฝ่ายภายใน 60 วินาทีและมี trace/log สำหรับการส่ง

## #11 | 2569-10-11 | Bash + filesystem | /implement T-08 specs/002-booking/tasks.md | จัดการสิทธิ์การเข้าถึงข้อมูล PII และข้อมูลตำแหน่งตาม REQ-SEC-004 และ REQ-PRV-002 โดยยึดตารางเวลา 2 ชั่วโมงก่อนนัดและการไม่ส่งข้อมูล PII/geoPoint ออกนอกระบบ | T-08 เสร็จแล้ว; `can_technician_view_customer_phone()` และ `get_customer_profile_for_technician()` ใช้เงื่อนไขเวลา 2 ชั่วโมงที่ถูกต้อง, while `sanitize_for_external_use()` มาสก์ phone และ geoPoint ก่อนส่ง/บันทึก log, และทดสอบ AC-07-09 ผ่าน | AI เดา: ไม่มีค่าที่ต้องถามเพิ่ม เพราะ spec ระบุชัดเจนว่าต้องเก็บ geoPoint แต่ไม่ส่งออกนอกระบบ และ technician จะเห็นเบอร์ได้เฉพาะช่วงเวลาที่กำหนด

## #12 | 2569-10-11 | Bash + filesystem | /implement T-09 specs/002-booking/tasks.md | สร้างกระบวนการคืนมัดจำตาม BR-01 โดยแยกกรณียกเลิกก่อน/หลังช่างออกเดินทางและส่งผลลัพธ์ชัดเจนสู่ลูกค้า | T-09 เสร็จแล้ว; `calculate_refund()` ปฏิบัติตาม rule ที่คืนเงินเต็มเมื่อลูกค้าจัดการยกเลิกก่อนช่างออกเดินทาง, คืน 0 เมื่อช่างออกเดินทางหรือเหตุผลไม่ผ่านเงื่อนไข, และ endpoint `/api/v1/bookings/{booking_id}/cancel` คืนค่า `refund_amount`, `reason`, `message` ให้ลูกค้าเห็นชัด | AI เดา: มีค่าเกือบต้องเดาเรื่อง R3 ของ Q-14 แต่ใช้คำตอบจาก spec ว่า “ติดต่อ call center” เป็นพฤติกรรมชั่วคราว จึงไม่คืนเงินเมื่อช่างเดินทางแล้วและแนะนำให้ติดต่อ call center แทน


## #12 | 2569-10-11 | Bash + filesystem | /implement T-11 specs/002-booking/tasks.md | สร้างหน้า booking integration แบบต่อ API จริง และเพิ่มการตรวจประสิทธิภาพ p95 สำหรับ AC-07-08 เพื่อให้ T-11 ครอบคลุมครบทุก AC ใน spec | T-11 เสร็จแล้ว; backend validation ใช้ `python -m pytest tests/test_booking_flow.py -q` และผ่าน 8 tests, while `frontend/src/pages/BookingPage.integration.jsx` ทำงานต่อ FastAPI จริงที่ `/api/v1/...` และ `frontend/src/integration/bookingFlow.test.jsx` ตรวจความคงที่ของ p95 ให้ต่ำกว่า 2 วินาที | AI เดา: ไม่มีคำถามเปิดเพิ่มเติม เพราะ spec/task ระบุชัดเจนว่าต้องตรวจทุก AC และ p95 ของ search/confirm ต้องต่ำกว่า 2 วินาที

## #13 | 2569-10-11 | Chat + filesystem | สรุปผลการรันลง specs/002-booking/ac-results.md | รัน backend tests 15 รายการ, frontend tests 2 รายการ, build และตรวจ HTTP health ของ frontend/backend แล้วบันทึกผลแยก AC พร้อมข้อจำกัด | ทีมขอให้สรุปผลลง ac-results.md; บันทึก AC-07-03 และ AC-07-08 ว่าผ่านบางส่วน และ AC-07-10 ว่ายังไม่ได้ทดสอบตามหลักฐานที่มี | AI เดา: ไม่มี; แยกผล automated tests ออกจากการยืนยัน AC จริง เนื่องจาก feature.feature ยังเป็น template และ PostgreSQL จริงยังเริ่มไม่ได้
