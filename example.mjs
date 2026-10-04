// Booking.com scraper API: nightly rates around a place, one typed row per property.
//
//   export QD_API_KEY=...        # https://app.quanticdata.io/register
//   node example.mjs "Roma, Italia" 2026-10-16 2026-10-17
//
// Node 18+, no dependencies.
// Docs and schema: https://quanticdata.io/collectors/booking-com-scraper-api/

const BASE = "https://api.quanticdata.io/v1";
const KEY = process.env.QD_API_KEY;
if (!KEY) {
  console.error("Set QD_API_KEY first: https://app.quanticdata.io/register");
  process.exit(1);
}
const headers = { Authorization: `Bearer ${KEY}`, "Content-Type": "application/json" };

const day = (offset) => new Date(Date.now() + offset * 86400000).toISOString().slice(0, 10);
const [location = "Roma, Italia", checkIn = day(14), checkOut = day(15)] = process.argv.slice(2);

const res = await fetch(`${BASE}/scraper/collectors/booking_stays/run`, {
  method: "POST",
  headers,
  body: JSON.stringify({
    location,
    check_in_date: checkIn,
    check_out_date: checkOut,
    adults: 2,
    currency: "EUR",
    max_results: 20,
  }),
});
const body = await res.json();
if (!res.ok || body.type === "error") {
  console.error(`Request failed (${res.status}): ${body.message}`);
  process.exit(1);
}
let run = body.payload;

// Long runs answer 202 and finish in the background: poll the run until it is done.
while (run.status === "queued" || run.status === "running") {
  await new Promise((r) => setTimeout(r, 3000));
  const s = await fetch(`${BASE}/scraper/collectors/runs/${run.run_id}`, { headers });
  run = (await s.json()).payload;
}

const rows = run.results ?? [];
console.table(
  rows.map((p) => ({
    rank: p.rank,
    name: p.name,
    price: p.price_value,
    currency: p.currency,
    discount_pct: p.discount_pct,
    score: p.review_score,
    reviews: p.review_count,
  })),
);
console.log(`${rows.length} properties for ${checkIn} to ${checkOut}`);
