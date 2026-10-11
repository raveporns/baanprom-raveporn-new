import { useEffect, useState } from 'react'
import { fetchAvailability, createBooking, payDeposit, cancelBooking } from '../mocks/bookingApi'

// REQ-FN-008, REQ-FN-041, REQ-IF-001, REQ-SEC-004
export default function BookingForm() {
  const [slots, setSlots] = useState([])
  const [selectedSlot, setSelectedSlot] = useState('')
  const [booking, setBooking] = useState(null)
  const [message, setMessage] = useState('')

  useEffect(() => {
    fetchAvailability().then((data) => {
      setSlots(data.slots)
      setSelectedSlot(data.slots[0]?.slotId ?? '')
    })
  }, [])

  const handleSubmit = async (event) => {
    event.preventDefault()
    const selected = slots.find((slot) => slot.slotId === selectedSlot)
    const result = await createBooking({
      customerId: 'cust-01',
      serviceType: 'repair',
      addressId: 'addr-01',
      technicianId: selected?.technicianId ?? 'tech-1',
      slotStart: selected?.start ?? '2026-10-05T09:00:00',
      slotEnd: selected?.end ?? '2026-10-05T10:00:00',
      depositAmount: 1500,
    })
    setBooking(result)
    setMessage('Booking created successfully')
  }

  const handlePayment = async () => {
    const payment = await payDeposit({ bookingId: booking?.id, amount: booking?.depositAmount ?? 1500 })
    setMessage(`Payment status: ${payment.gatewayStatus}`)
  }

  const handleCancel = async () => {
    const refund = await cancelBooking(booking?.id ?? 'booking-0001')
    setMessage(`Cancellation processed: refund ${refund.refundAmount} THB`)
  }

  return (
    <form className="space-y-6" onSubmit={handleSubmit}>
      <div className="space-y-2">
        <label className="text-sm font-semibold text-slate-700">Select technician slot</label>
        <select
          value={selectedSlot}
          onChange={(event) => setSelectedSlot(event.target.value)}
          className="w-full rounded-xl border border-slate-300 bg-white px-3 py-2 text-sm outline-none ring-0"
        >
          {slots.map((slot) => (
            <option key={slot.slotId} value={slot.slotId}>
              {slot.technicianId} — {slot.start} to {slot.end}
            </option>
          ))}
        </select>
      </div>

      <button type="submit" className="w-full rounded-xl bg-blue-600 px-4 py-3 text-sm font-semibold text-white shadow-sm hover:bg-blue-700">
        Create booking
      </button>

      {booking && (
        <div className="rounded-xl border border-slate-200 bg-slate-50 p-4 text-sm text-slate-700">
          <p><strong>Booking ID:</strong> {booking.id}</p>
          <p><strong>Technician:</strong> {booking.technicianId}</p>
          <p><strong>Deposit:</strong> {booking.depositAmount} THB</p>
        </div>
      )}

      <div className="flex gap-3">
        <button type="button" onClick={handlePayment} className="flex-1 rounded-xl border border-emerald-200 bg-emerald-50 px-4 py-3 text-sm font-semibold text-emerald-700">
          Pay deposit
        </button>
        <button type="button" onClick={handleCancel} className="flex-1 rounded-xl border border-rose-200 bg-rose-50 px-4 py-3 text-sm font-semibold text-rose-700">
          Cancel booking
        </button>
      </div>

      {message && <p className="text-sm text-slate-700">{message}</p>}
    </form>
  )
}
