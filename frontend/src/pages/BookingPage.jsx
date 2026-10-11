import BookingForm from '../components/BookingForm'

// REQ-FN-008, REQ-FN-041, REQ-IF-001, REQ-SEC-004
export default function BookingPage() {
  return (
    <main className="min-h-screen bg-slate-100 px-4 py-10 text-slate-900">
      <div className="mx-auto max-w-4xl rounded-2xl border border-slate-200 bg-white shadow-lg">
        <div className="border-b border-slate-200 bg-slate-50 px-6 py-5">
          <p className="text-xs font-semibold uppercase tracking-[0.2em] text-blue-600">Booking</p>
          <h1 className="mt-2 text-3xl font-bold">จองงานบริการซ่อมบำรุง</h1>
        </div>

        <div className="grid gap-8 p-6 lg:grid-cols-[1.4fr_0.6fr]">
          <BookingForm />

          <aside className="space-y-4 rounded-xl border border-slate-200 bg-slate-50 p-5">
            <h2 className="text-lg font-semibold">Policy summary</h2>
            <ul className="space-y-2 text-sm text-slate-700">
              <li>• Search available technicians within 7 days</li>
              <li>• 10-minute temporary lock</li>
              <li>• Deposit paid through payment gateway</li>
              <li>• Customer and technician notified within 60 seconds</li>
              <li>• Refund follows BR-01</li>
            </ul>
          </aside>
        </div>
      </div>
    </main>
  )
}
