// REQ-FN-008, REQ-FN-041, REQ-IF-001, REQ-BR-001
export const mockTechnicians = [
  { id: 'tech-1', name: 'ช่าง A', rating: 4.9, serviceType: 'repair' },
  { id: 'tech-2', name: 'ช่าง B', rating: 4.8, serviceType: 'repair' },
  { id: 'tech-3', name: 'ช่าง C', rating: 4.7, serviceType: 'repair' },
]

export const mockAvailableSlots = [
  { slotId: 'slot-1', technicianId: 'tech-1', start: '2026-10-05T09:00:00', end: '2026-10-05T10:00:00', available: true },
  { slotId: 'slot-2', technicianId: 'tech-2', start: '2026-10-05T10:00:00', end: '2026-10-05T11:00:00', available: true },
  { slotId: 'slot-3', technicianId: 'tech-3', start: '2026-10-05T11:00:00', end: '2026-10-05T12:00:00', available: true },
]

// REQ-FN-008
export async function fetchAvailability() {
  return { slots: mockAvailableSlots }
}

// REQ-FN-041, REQ-IF-001
export async function createBooking(payload) {
  return {
    id: 'booking-0001',
    ...payload,
    status: 'confirmed',
  }
}

// REQ-IF-001
export async function payDeposit(payload) {
  return {
    bookingId: payload.bookingId,
    amount: payload.amount,
    gatewayStatus: 'captured',
    gatewayRef: 'gw-0001',
    message: 'Payment captured successfully',
  }
}

// REQ-BR-001
export async function cancelBooking(bookingId) {
  return {
    bookingId,
    refundAmount: 1500,
    rule: 'BR-01',
    status: 'processed',
  }
}
