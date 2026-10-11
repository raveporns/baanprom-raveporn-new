# Tasks: การจองงานบริการซ่อมบำรุง

- Feature: การจองงานบริการซ่อมบำรุง (SPEC-BOOKING)
- Spec ID: SPEC-BOOKING
- อ้างอิง: plan.md
- วันที่: 2569-10-04
- สรุป: มี 11 task รวมงานพื้นฐานและตรวจสอบ, 4 task ที่ต้องรอ Open Questions (Q-14, Q-18, Q-19, Q-22)
- เทคโนโลยีที่เลือก: Frontend = React + Vite + Tailwind CSS, Backend = FastAPI, Database = PostgreSQL

## T-01 ตั้งโครงโปรเจกต์ booking
- รองรับ: REQ-CON-001, REQ-CON-003
- ตรวจด้วย: ไม่มี AC ตรง ๆ เป็นงานพื้นฐานของ T-01
- ไฟล์ที่แตะ: frontend/package.json, frontend/vite.config.*, frontend/src/, backend/app/, backend/requirements.txt, backend/.env.example, docker-compose.yml, db/migrations/
- ต้องทำหลัง: ไม่มี
- เสร็จเมื่อ: รัน test เปล่าผ่าน 1 ตัว และโครงโปรเจกต์พร้อมใช้งานสำหรับฟีเจอร์ booking ด้วย stack React + Vite + Tailwind, FastAPI, PostgreSQL
- สถานะ: เสร็จแล้ว (frontend build pass + backend smoke test pass)

## T-02 สร้างโมเดลข้อมูล Job/TimeSlot/Payment/Refund
- รองรับ: REQ-DAT-002, REQ-PRV-002, REQ-SEC-004, REQ-FN-041
- ตรวจด้วย: AC-07-04, AC-07-09
- ไฟล์ที่แตะ: backend/app/models/*.py, backend/app/schemas/*.py, db/migrations/, backend/app/services/security.py
- ต้องทำหลัง: T-01
- เสร็จเมื่อ: job, timeslot, payment, refund และ history state model พร้อมกำหนดสถานะและข้อมูล PII อย่างชัดเจน
- สถานะ: เสร็จ รอทีมตรวจ

## T-03 สร้าง API ค้นหาช่างว่างและแสดงราคา/เงื่อนไข
- รองรับ: REQ-FN-008
- ตรวจด้วย: AC-07-01, AC-07-02
- ไฟล์ที่แตะ: backend/app/api/booking.py, backend/app/services/availability.py, backend/app/schemas/booking.py
- ต้องทำหลัง: T-02
- เสร็จเมื่อ: API คืนช่างที่ว่างภายใน 7 วัน พร้อมข้อมูลประเภทงาน/ที่อยู่/ช่วงเวลาและราคามัดจำที่เห็นได้จากลูกค้า
- สถานะ: เสร็จ รอทีมตรวจ

## T-04 สร้างล็อกช่วงเวลาและหมดอายุอัตโนมัติ
- รองรับ: REQ-FN-041
- ตรวจด้วย: AC-07-04, AC-07-08
- ไฟล์ที่แตะ: backend/app/services/booking_lock.py, backend/app/tasks/lock_expiry.py, db/migrations/...
- ต้องทำหลัง: T-03
- เสร็จเมื่อ: ระบบล็อกช่วงเวลาไว้ระหว่างขั้นยืนยันและปลดล็อกอัตโนมัติเมื่อหมดอายุแล้วโดยไม่ให้ซ้อนทับ
- สถานะ: เสร็จ รอทีมตรวจ

## T-05 สร้างกระบวนการชำระมัดจำผ่าน Payment Gateway
- รองรับ: REQ-IF-001, REQ-IF-005, REQ-CON-003
- ตรวจด้วย: AC-07-05, AC-07-06, AC-07-07
- ไฟล์ที่แตะ: backend/app/services/payment.py, backend/app/integrations/payment_gateway.py, backend/app/api/checkout.py
- ต้องทำหลัง: T-04
- เสร็จเมื่อ: ระบบ authorize แล้ว capture มัดจำผ่าน gateway ได้ และเมื่อ timeout จึงเรียก status inquiry ด้วย reference เดิม
- สถานะ: เสร็จ รอทีมตรวจ

## T-06 สร้างงานยืนยันแล้วและ lifecycle ของ Job
- รองรับ: REQ-DAT-002, REQ-FN-012
- ตรวจด้วย: AC-07-03
- ไฟล์ที่แตะ: backend/app/services/job_creation.py, backend/app/models/job.py, backend/app/repositories/job_repository.py
- ต้องทำหลัง: T-05
- เสร็จเมื่อ: หลังชำระสำเร็จระบบสร้างงานในสถานะยืนยันแล้ว และเก็บประวัติการเปลี่ยนสถานะ 24 เดือนตาม MD-STM-01
- สถานะ: เสร็จ รอทีมตรวจ

## T-07 สร้างการแจ้งลูกค้าและช่างหลังสร้างงาน
- รองรับ: REQ-FN-012, REQ-IF-002
- ตรวจด้วย: AC-07-03
- ไฟล์ที่แตะ: backend/app/services/notifications.py, backend/app/integrations/sms.py, backend/app/events/job_created.py
- ต้องทำหลัง: T-06
- เสร็จเมื่อ: แจ้งทั้งสองฝ่ายภายใน 60 วินาทีหลังสร้างงานและมี log/trace สำหรับการส่งแจ้งเตือน
- สถานะ: เสร็จ รอทีมตรวจ

## T-08 จัดการสิทธิ์การเข้าถึงข้อมูล PII และข้อมูลตำแหน่ง
- รองรับ: REQ-SEC-004, REQ-PRV-002
- ตรวจด้วย: AC-07-09
- ไฟล์ที่แตะ: backend/app/security/access_control.py, backend/app/validators/pii.py, backend/app/services/customer_profile.py
- ต้องทำหลัง: T-02
- เสร็จเมื่อ: ช่างเห็นเบอร์ลูกค้าเฉพาะช่วงเวลาที่กำหนดเท่านั้น และไม่เก็บ/ส่งข้อมูล PII ลง log หรือออกนอกระบบตามกฎ
- สถานะ: เสร็จ รอทีมตรวจ

## T-09 สร้างกระบวนการคืนมัดจำตาม BR-01
- รองรับ: REQ-BR-001
- ตรวจด้วย: AC-07-10
- ไฟล์ที่แตะ: backend/app/services/refund.py, backend/app/rules/refund_policy.py, backend/app/api/cancel_booking.py
- ต้องทำหลัง: T-06
- เสร็จเมื่อ: กระบวนการยกเลิกและคืนมัดจำให้สอดคล้องกับ decision table BR-01 และมีผลลัพธ์ที่ชัดเจนต่อลูกค้า
- สถานะ: เสร็จ รอทีมตรวจ

## T-10 สร้างหน้า booking แบบ mock API
- รองรับ: REQ-FN-008, REQ-FN-041, REQ-IF-001, REQ-SEC-004
- ตรวจด้วย: AC-07-01, AC-07-02, AC-07-04, AC-07-09
- ไฟล์ที่แตะ: frontend/src/pages/BookingPage.jsx, frontend/src/components/BookingForm.jsx, frontend/src/mocks/bookingApi.js
- ต้องทำหลัง: ไม่มี
- เสร็จเมื่อ: หน้า booking ทำงานได้แบบ mock และให้ลูกค้าเลือกช่าง/ช่วงเวลา/เงื่อนไขก่อนยืนยันหรือชำระ
- สถานะ: เสร็จ รอทีมตรวจ

## T-11 ต่อหน้าจอกับ API จริง และตรวจประสิทธิภาพ/AC ครบชุด
- รองรับ: REQ-QA-003 และทุก AC ใน spec
- ตรวจด้วย: AC-07-01, AC-07-02, AC-07-03, AC-07-04, AC-07-05, AC-07-06, AC-07-07, AC-07-08, AC-07-09, AC-07-10
- ไฟล์ที่แตะ: frontend/src/integration/bookingFlow.test.jsx, backend/tests/test_booking_flow.py, frontend/src/pages/BookingPage.integration.jsx
- ต้องทำหลัง: T-03, T-05, T-07, T-08, T-09, T-10
- เสร็จเมื่อ: ทุก AC ผ่าน และประเมิน p95 ของค้นหา/ยืนยันได้ไม่เกิน 2 วินาทีสำหรับผู้ใช้ 500 คนพร้อมกัน
- สถานะ: เสร็จ รอทีมตรวจ

## ตารางตรวจความครบ AC

| AC ID | task ที่ตรวจ AC นี้ |
|---|---|
| AC-07-01 | T-03, T-10 |
| AC-07-02 | T-03, T-10 |
| AC-07-03 | T-06, T-07 |
| AC-07-04 | T-04, T-10 |
| AC-07-05 | T-05 |
| AC-07-06 | T-05 |
| AC-07-07 | T-05 |
| AC-07-08 | T-04, T-11 |
| AC-07-09 | T-08, T-10 |
| AC-07-10 | T-09 |

## ตารางตรวจความครบ Constraint

| Constraint ID | task ที่ทำให้เป็นจริง |
|---|---|
| REQ-CON-001 | T-01 |
| REQ-CON-003 | T-05 |

## สิ่งที่ยังไม่ทำ

- Q-14: BR-01 R3 ลูกค้ายกเลิกขณะช่างเดินทาง คืนเท่าไร — รอ task T-09 และต้องตอบจาก SH-01 ก่อนทำต่อ
- Q-18: ล็อกช่วงเวลาชั่วคราวนานเท่าไร — รอ task T-04 และต้องตอบจาก Ops lead ก่อนทำต่อ
- Q-19: gateway-timeout ตามสัญญาคือกี่วินาที — รอ task T-05 และต้องตอบจาก Dev lead ก่อนทำต่อ
- Q-22: ServiceAddress.geoPoint ต้องมี REQ-PRV ไหม — รอ task T-08 และต้องตอบจาก RE lead ก่อนทำต่อ
