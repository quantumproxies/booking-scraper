# Booking.com scraper API — examples

Nightly rates around any address, for the dates you ask for. One POST returns one typed row per property: the price for that exact stay, the struck-through price and the discount it implies, review score, star class, room type and coordinates.

**Live page, full schema and pricing: [quanticdata.io/collectors/booking-com-scraper-api/](https://quanticdata.io/collectors/booking-com-scraper-api/)**

Runnable examples in [Python](example.py) and [Node.js](example.mjs), plus a [real response](sample-response.json) captured from the API.

## Quick start (curl)

```bash
curl -X POST https://api.quanticdata.io/v1/scraper/collectors/booking_stays/run \
  -H "Authorization: Bearer $QD_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"location":"Roma, Italia","check_in_date":"2026-10-16","check_out_date":"2026-10-17","adults":2,"currency":"EUR","lang":"it","country":"it","max_results":20}'
```

## Python

```bash
pip install requests
export QD_API_KEY=qd_live_your_key_here   # https://app.quanticdata.io/register
python3 example.py "Roma, Italia" 2026-10-16 2026-10-17
```

## Node.js

Node 18 or newer, no dependencies.

```bash
export QD_API_KEY=qd_live_your_key_here
node example.mjs "Roma, Italia" 2026-10-16 2026-10-17
```

Both scripts default to a one-night stay two weeks from today when you pass no dates.

## Inputs

| Input | Type | Required | What it does |
|---|---|---|---|
| `location` | string | no | City, area or street address, e.g. "Roma, Italia" or "12 Marine Parade, Napier, New Zealand". Resolved to coordinates first; pass `latitude`/`longitude` instead to skip that step. |
| `latitude` | number | no | Alternative to `location`. |
| `longitude` | number | no | Alternative to `location`. |
| `check_in_date` | string | yes | YYYY-MM-DD |
| `check_out_date` | string | yes | YYYY-MM-DD, after check-in |
| `adults` | integer | no | Guests (1-30). |
| `rooms` | integer | no | Rooms (1-10). |
| `currency` | string | no | Price currency (EUR, USD, NZD...). |
| `country` | string | no | ISO 3166-1 alpha-2 code. |
| `lang` | string | no | Interface language, e.g. en, it, de. |
| `max_results` | integer | no | How many properties to deliver at most (1-100). You pay only for delivered properties. |

## Output: one row per property

| Field | Type | What it holds |
|---|---|---|
| `rank` | integer | 1-based position in Booking's order. |
| `name` | string | Property name. |
| `property_id` | integer | Booking's own property id. |
| `price` | string | Nightly price as shown. |
| `price_value` | number | Numeric price for the stay requested, taxes and fees included. |
| `currency` | string | Currency of the price. |
| `strikethrough_value` | number | Price before the discount, when Booking shows one. |
| `discount_pct` | integer | Discount implied by the two prices. |
| `review_score` | number | Guest score out of 10. |
| `review_word` | string | Booking's word for that score. |
| `review_count` | integer | Number of reviews. |
| `stars` | integer | Star class. |
| `room_type` | string | The unit Booking recommends for this stay. |
| `area` | string | Neighbourhood as Booking names it. |
| `distance_m` | integer | Metres from the point you searched. |
| `free_cancellation` | boolean | Free-cancellation badge on this offer. |
| `breakfast_included` | boolean | Breakfast is included in this price. |
| `rooms_left_at_price` | integer | "We have N left at this price", when Booking says so. |
| `taxes_included` | boolean | Whether the price already includes taxes and charges. |
| `latitude`, `longitude` | number | Property coordinates. |
| `checkin_from`, `checkout_until` | string | Earliest check-in and latest check-out time. |
| `photo`, `photos` | string, string[] | Main photo URL and every photo on the card. |
| `check_in_date`, `check_out_date` | string | Echo of the request. |

Nullable means the source did not publish it: the field stays empty instead of being guessed. The full list, with `distance_text`, `sustainability`, `preferred`, `quality_class` and `country`, is on the [live page](https://quanticdata.io/collectors/booking-com-scraper-api/#output).

## Sample response

A real run from 4 October 2026: Rome, one night from 16 October, two adults, three rows requested. The rows arrive in `payload.results`; one of the three is shown here and all three are in [`sample-response.json`](sample-response.json).

```json
{
  "rank": 2,
  "name": "Hotel Castellino Roma",
  "property_id": 81897,
  "price": "€ 385",
  "price_value": 384.89,
  "currency": "EUR",
  "strikethrough_value": 471.66,
  "discount_pct": 18,
  "review_score": 8.5,
  "review_word": "Ottimo",
  "review_count": 1681,
  "stars": 4,
  "room_type": "Camera di hotel: Letti: 1 matrimoniale o 2 singoli",
  "taxes_included": true,
  "preferred": true,
  "latitude": 41.8968073592107,
  "longitude": 12.4823979518605,
  "country": "it",
  "checkin_from": "15:00",
  "checkout_until": "10:30",
  "photo": "https://cf.bstatic.com/xdata/images/hotel/square60/323161059.jpg",
  "check_in_date": "2026-10-16",
  "check_out_date": "2026-10-17"
}
```

Fields that came back `null` on this row are left out of the excerpt above; the JSON file keeps them.

Every response uses the same envelope: `{"type": "response", "message": "...", "payload": {...}}` on success, `{"type": "error", "message": "..."}` on failure. Long runs answer `202` and are read from `GET /v1/scraper/collectors/runs/{run_id}`; both examples handle that.

## Pricing

**$0.02 per delivered property** ($20 per 1,000). A run that delivers nothing costs nothing. Every account gets $2 of free credit each month with no card, which is about 100 delivered properties on this endpoint. `GET /v1/scraper/collectors` returns the price your key actually pays.

## Links

- This collector: https://quanticdata.io/collectors/booking-com-scraper-api/
- All collectors: https://quanticdata.io/collectors/
- API reference: https://quanticdata.io/docs/
- OpenAPI: https://quanticdata.io/docs/openapi.yaml

## License

MIT. Use the data in line with the terms of the sites it comes from and the laws that apply to you.
