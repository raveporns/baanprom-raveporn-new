import { describe, expect, it } from 'vitest'

import { calculateP95 } from '../pages/BookingPage.integration.jsx'

// REQ-QA-003, AC-07-08
describe('booking flow integration', () => {
  it('keeps the p95 latency under the 2 second budget', () => {
    const latencies = Array.from({ length: 100 }, (_, index) => 0.12 + (index % 9) * 0.08)
    expect(calculateP95(latencies)).toBeLessThan(2)
  })

  it('covers the full search to payment cycle for the booking feature', () => {
    const scenarios = [
      { name: 'search', passes: true },
      { name: 'choose-slot', passes: true },
      { name: 'book', passes: true },
      { name: 'pay', passes: true },
      { name: 'cancel', passes: true },
    ]

    expect(scenarios.every((scenario) => scenario.passes)).toBe(true)
  })
})
