import { useEffect, useState } from 'react'

const API_BASE = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000'

export function calculateP95(samples) {
  if (!samples.length) return 0
  const sorted = [...samples].sort((left, right) => left - right)
  const index = Math.max(0, Math.ceil(sorted.length * 0.95) - 1)
  return Number(sorted[index].toFixed(3))
}

async function requestJson(path, options = {}) {
  const response = await fetch(`${API_BASE}${path}`, {
    headers: { 'Content-Type': 'application/json', ...(options.headers ?? {}) },
    ...options,
  })

  if (!response.ok) {
    const message = await response.text()
    throw new Error(message || `Request failed for ${path}`)
  }

  return response.json()
}

export async function runBookingFlowScenario() {
  const availabilityStart = performance.now()
  const availability = await requestJson('/api/v1/availability?service_type=repair&date=2026-10-05T00:00:00')
  const availabilityMs = performance.now() - availabilityStart

  const slot = availability.slots?.[0]
  if (!slot) {
    throw new Error('No availability slots were returned for the booking flow')
  }

  const bookingResponse = await requestJson('/api/v1/bookings', {
    method: 'POST',
    body: JSON.stringify({
      customer_id: 'cust-01',
      service_type: 'repair',
      address_id: 'addr-01',
      technician_id: slot.technician_id,
      slot_start: slot.start,
      slot_end: slot.end,
      deposit_amount: slot.deposit_amount,
    }),
  })

  const paymentResponse = await requestJson(
    `/api/v1/checkout?booking_id=${bookingResponse.id}&amount=${slot.deposit_amount}`,
    { method: 'POST' },
  )

  const cancellationResponse = await requestJson(
    `/api/v1/bookings/${bookingResponse.id}/cancel?reason=customer_cancelled`,
    { method: 'POST' },
  )

  return {
    availabilityMs,
    bookingId: bookingResponse.id,
    paymentStatus: paymentResponse.gateway_status,
    refundAmount: cancellationResponse.refund_amount,
    slots: availability.slots.length,
  }
}

// REQ-QA-003, REQ-FN-008, REQ-FN-041, REQ-IF-001, REQ-BR-001
export default function BookingPageIntegration() {
  const [slots, setSlots] = useState([])
  const [selectedSlot, setSelectedSlot] = useState('')
  const [booking, setBooking] = useState(null)
  const [result, setResult] = useState(null)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    let active = true

    async function loadAvailability() {
      try {
        const payload = await requestJson('/api/v1/availability?service_type=repair&date=2026-10-05T00:00:00')
        if (!active) return
        const nextSlots = payload.slots ?? []
        setSlots(nextSlots)
        setSelectedSlot(nextSlots[0]?.slot_id ?? '')
      } catch (loadError) {
        if (active) {
          setError(loadError.message)
        }
      } finally {
        if (active) {
          setLoading(false)
        }
      }
    }

    loadAvailability()
    return () => {
      active = false
    }
  }, [])

  const handleCreateBooking = async () => {
    if (!selectedSlot) return
    const slot = slots.find((entry) => entry.slot_id === selectedSlot)

    try {
      const bookingResponse = await requestJson('/api/v1/bookings', {
        method: 'POST',
        body: JSON.stringify({
          customer_id: 'cust-01',
          service_type: 'repair',
          address_id: 'addr-01',
          technician_id: slot.technician_id,
          slot_start: slot.start,
          slot_end: slot.end,
          deposit_amount: slot.deposit_amount,
        }),
      })

      setBooking(bookingResponse)
      setError('')
    } catch (submitError) {
      setError(submitError.message)
    }
  }

  const handleCheckout = async () => {
    if (!booking) return

    try {
      const paymentResponse = await requestJson(
        `/api/v1/checkout?booking_id=${booking.id}&amount=${booking.deposit_amount}`,
        { method: 'POST' },
      )
      setResult({ stage: 'payment', payload: paymentResponse })
    } catch (paymentError) {
      setError(paymentError.message)
    }
  }

  const handleCancel = async () => {
    if (!booking) return

    try {
      const cancellation = await requestJson(`/api/v1/bookings/${booking.id}/cancel?reason=customer_cancelled`, {
        method: 'POST',
      })
      setResult({ stage: 'cancel', payload: cancellation })
    } catch (cancelError) {
      setError(cancelError.message)
    }
  }

  return (
    <main className="mx-auto max-w-3xl p-6 text-slate-900">
      <h1 className="text-3xl font-bold">Booking flow integration</h1>
      <p className="mt-2 text-sm text-slate-600">
        Validates the full booking lifecycle against the live FastAPI backend.
      </p>

      {loading ? (
        <p className="mt-6 text-sm text-slate-700">Loading availability…</p>
      ) : (
        <div className="mt-6 space-y-4 rounded-xl border border-slate-200 bg-white p-5 shadow-sm">
          <label className="block text-sm font-semibold text-slate-700">Choose available slot</label>
          <select
            value={selectedSlot}
            onChange={(event) => setSelectedSlot(event.target.value)}
            className="w-full rounded-xl border border-slate-300 px-3 py-2 text-sm"
          >
            {slots.map((slot) => (
              <option key={slot.slot_id} value={slot.slot_id}>
                {slot.technician_id} — {slot.start} to {slot.end} ({slot.deposit_amount} THB)
              </option>
            ))}
          </select>

          <div className="flex gap-3">
            <button
              type="button"
              onClick={handleCreateBooking}
              className="rounded-xl bg-blue-600 px-4 py-2 text-sm font-semibold text-white"
            >
              Create booking
            </button>
            <button
              type="button"
              onClick={handleCheckout}
              className="rounded-xl border border-emerald-200 bg-emerald-50 px-4 py-2 text-sm font-semibold text-emerald-700"
            >
              Pay deposit
            </button>
            <button
              type="button"
              onClick={handleCancel}
              className="rounded-xl border border-rose-200 bg-rose-50 px-4 py-2 text-sm font-semibold text-rose-700"
            >
              Cancel
            </button>
          </div>

          {booking && (
            <div className="rounded-lg border border-slate-200 bg-slate-50 p-3 text-sm text-slate-700">
              <p><strong>Booking ID:</strong> {booking.id}</p>
              <p><strong>Technician:</strong> {booking.technician_id}</p>
              <p><strong>Deposit:</strong> {booking.deposit_amount} THB</p>
            </div>
          )}

          {result && (
            <div className="rounded-lg border border-slate-200 bg-slate-50 p-3 text-sm text-slate-700">
              <p><strong>Stage:</strong> {result.stage}</p>
              <p><strong>Status:</strong> {result.payload.gateway_status ?? result.payload.status}</p>
              <p><strong>Refund:</strong> {result.payload.refund_amount ?? 'n/a'}</p>
            </div>
          )}

          {error && <p className="text-sm text-rose-600">{error}</p>}
        </div>
      )}
    </main>
  )
}
