# SPEC-BOOKING | การจองงานบริการซ่อมบำรุง (UC-07)

version: 1.0 | status: baselined (B1) | owner: กลุ่ม X / PO: SH-01 | date: 2569-09-06
baseline: B1 (2569-09-06) | supersedes: | related: SPEC-CANCEL (draft) | feature file: booking.feature v1.0

## Change Log

| เวอร์ชัน | วันที่ | เปลี่ยนอะไร | เพราะอะไร | ใคร |
|---|---|---|---|---|
| 1.0 (v1) | 2569-09-06 | ประกอบ 11 ส่วนจาก catalogue, UC-07, booking.feature, models, rules เข้า Baseline B1 | บทเรียน Living Specification | กลุ่ม X |

## 1. Intent

ลูกค้าที่มีงานซ่อมด่วนต้องได้ช่างที่ว่างจริงในเวลาที่ต้องการโดยไม่ต้องโทรถาม (PB-02, EV-004, EV-009)
ปัจจุบัน call center รับสายถามสถานะราว 30 ถึง 40 สายต่อวัน (EV-012)
และการยกเลิกหลังวางมัดจำไม่มีนโยบายเป็นลายลักษณ์อักษร (EV-023) feature นี้ทำให้การจอง การวางมัดจำ และเงื่อนไขยกเลิก
เป็นขั้นตอนเดียวที่ระบบคุมเองทั้งหมด

## 2. Scope และ Non-goals

In: ค้นช่างว่าง | ล็อกช่วงเวลาชั่วคราว | แสดงราคา มัดจำ เงื่อนไข | ชำระมัดจำผ่าน gateway | สร้างงาน "ยืนยันแล้ว" | แจ้งสองฝ่าย | คืนมัดจำตาม BR-01 เมื่อยกเลิก

Non-goals (R1):
- ระบบแนะนำช่างอัตโนมัติ (REQ-AI-002 | Won't R1 | รอข้อมูล 3 เดือน)
- รีวิวและให้คะแนนช่าง (UC-11 นอกขอบเขต R1 ไม่มี EV รองรับ; Technician.rating ยังเป็น CC-06 เปิด)
- จองโดยไม่ลงทะเบียน (Q-05 ยังไม่ตัดสิน พฤติกรรมชั่วคราว: ต้องลงทะเบียนก่อน)
- การจับคู่ช่างใหม่เมื่อช่างปฏิเสธ (UC-05) feature นี้แค่เปลี่ยนสถานะงานเป็น "กำลังหาช่างใหม่"
- จองแทนลูกค้าโดย call center (A2) เลื่อนไป R2 ตามมติ 6 ก.ย. (D-07-02)

## 3. Actors และ Context

ลูกค้าที่ลงทะเบียน (primary) | ช่าง | Payment Gateway (IF-01) | ระบบส่งข้อความ (IF-02) | บริการแผนที่ (IF-03) ดู MD-CTX-01 ใน models.md

## 4. Requirements

ข้อความต้นฉบับอยู่ใน docs/srs/catalogue.md ห้ามแก้ที่นี่

| ID | สรุป | MoSCoW | Conf. | AC | หมายเหตุ |
|---|---|---|---|---|---|
| REQ-FN-008 | ลูกค้าจองงานโดยเลือกประเภท ที่อยู่ ช่าง ช่วงเวลา จากช่างที่ว่างใน 7 วัน | Must | High | AC-07-01, AC-07-02 | |
| REQ-FN-041 | ล็อกช่วงเวลาชั่วคราวระหว่างขั้น 3 ถึง 5 (derived MD-ACT-07) | Must | Low | AC-07-04 | ระยะล็อก = Q-18 |
| REQ-FN-012 | แจ้งลูกค้าและช่างภายใน 60 วินาทีหลังสร้างงาน | Must | High | AC-07-03 | |
| REQ-BR-001 | คืนมัดจำตาม BR-01 (Decision Table R1 ถึง R6) | Must | Low | AC-07-10 (Outline) | R3 รอ Q-14 |
| REQ-IF-001 | ตัดมัดจำผ่าน Payment Gateway ตาม IF-01 (authorize แล้ว capture) | Must | Med | AC-07-05, AC-07-06 | |
| REQ-IF-005 | status-inquiry ด้วย reference เดิมเมื่อ gateway ไม่ตอบใน gateway-timeout | Must | Low | AC-07-05, AC-07-07 | ค่า timeout = Q-19 |
| REQ-QA-003 | ขั้นตอนค้นหาและยืนยันไม่เกิน 2 วินาที p95 ที่ผู้ใช้พร้อมกัน 500 คน | Should | Med | AC-07-08 | |
| REQ-SEC-004 | ช่างเห็นเบอร์ลูกค้าเฉพาะ 2 ชั่วโมงก่อนนัดจนปิดงาน | Must | High | AC-07-09 | |
| REQ-PRV-002 | เบอร์โทรลูกค้าเป็น PII ห้ามลง log | Must | High | AC-07-09 | |
| REQ-DAT-002 | งานมีสถานะตาม MD-STM-01 (8 สถานะ) เก็บประวัติ 24 เดือน | Must | High | (ตรวจผ่าน T-01) | |

## 5. Behaviour

- Use case: UC-07 (fully dressed, docs/srs/UC-07.md) | main path 6 ขั้น | A1, A2 (A2 เลื่อนไป R2), E1 ถึง E3
- วงจรชีวิตของงาน: MD-STM-01 (8 สถานะ, CC-01 ปิดแล้ว)
- กฎธุรกิจ: BR-01 (คืนมัดจำ) | BR-02 (ช่างไม่รับงานซ้อน) | BR-03 (ระยะให้บริการ 15 กิโลเมตร) ใน rules.md
- ลำดับการชำระ: MD-SEQ-07-05
- ใช้ชื่อสถานะตาม docs/srs/glossary.md เท่านั้น

## 6. Acceptance Criteria

ไฟล์ booking.feature (AC-07-01 ถึง AC-07-10)
ครบเมื่อ: ทุก path ใน UC-07 มี scenario | ทุกแถว BR-01 มี example | ไม่มี Then ที่มองไม่เห็นจากภายนอก

## 7. Data

Job(status, depositAmount, scheduledStart) | TimeSlot(state, holdExpiresAt) | Payment(result, gatewayRef) | Refund(amount, rule)
Customer.phone เป็น PII (REQ-PRV-002) | ServiceAddress.geoPoint เป็น PII ไม่มี REQ-PRV รองรับ (Q-22)
เก็บประวัติการเปลี่ยนสถานะงาน 24 เดือน (REQ-DAT-002)

## 8. Constraints

- REQ-CON-001 R1 = 8 สัปดาห์ ทีม 4 คน
- REQ-CON-003 ต้องใช้ Payment Gateway รายเดิมตามสัญญาถึงธันวาคม 2569
- ไม่มีข้อจำกัดเรื่องภาษาหรือ framework ใน spec (ทีมเลือกเอง ดู plan.md ข้อ 2)
- ทีมเลือกเอง (ไม่ได้มาจาก spec): Frontend = React + Vite + Tailwind CSS, Backend = FastAPI, Database = PostgreSQL

## 9. Open Questions และ Assumptions

| ID | คำถาม / สมมติฐาน | เจ้าของ | กำหนด | พฤติกรรมชั่วคราว |
|---|---|---|---|---|
| Q-14 | BR-01 R3 ลูกค้ายกเลิกขณะช่างเดินทาง คืนเท่าไร | SH-01 | 13 ก.ย. | ไม่อนุญาตให้ยกเลิก ตอบ "ติดต่อ call center" |
| Q-18 | ล็อกช่วงเวลาชั่วคราวนานเท่าไร | Ops lead | 13 ก.ย. |ตอบ 10 นาที |
| Q-19 | gateway-timeout ตามสัญญาคือกี่วินาที | Dev lead | 13 ก.ย. | 30 วินาที |
| Q-22 | ServiceAddress.geoPoint ต้องมี REQ-PRV ไหม | RE lead | 13 ก.ย. | เก็บ แต่ไม่ส่งออกนอกระบบ |
| AS-03 | ลูกค้าหนึ่งคนมีที่อยู่ให้บริการได้หลายที่ | | | โมเดลรองรับ 1..* |

## 10. Decision Log

| ID | ตัดสินใจอะไร | ทางเลือกที่ปฏิเสธ | ผู้ตัดสิน | วันที่ |
|---|---|---|---|---|
| D-07-01 | ล็อกช่วงเวลาตั้งแต่ขั้น 3 ไม่ใช่ขั้น 5 (ต้องมี REQ-FN-041) | ตรวจซ้ำตอนชำระเท่านั้น (E2 เกิดบ่อย) | กลุ่ม X + SH-01 | 6 ก.ย. |
| D-07-02 | A2 จองแทนโดย call center เลื่อนไป R2 | ทำใน R1 (ติด REQ-CON-001) | SH-01 | 6 ก.ย. |

## 11. AI Disclosure

ร่างส่วน 4 ถึง 6 ด้วย AI จาก UC-07 + catalogue (prompt-log.md #12 ถึง #15) ตรวจโดยสมาชิก A, B
สิ่งที่ AI เดาแล้วถูกตัด: ระยะล็อก 15 นาที, สถานะ "รอรีวิว"
