# Booking.com Scraper

[![ci](https://github.com/quantumproxies/booking-scraper/actions/workflows/ci.yml/badge.svg)](https://github.com/quantumproxies/booking-scraper/actions/workflows/ci.yml) ![python](https://img.shields.io/badge/python-3.9%2B-blue) ![license](https://img.shields.io/badge/license-MIT-green) ![dependencies](https://img.shields.io/badge/dependencies-none-brightgreen)

Scrape Booking.com from Python or the command line: the hotels, apartments and B&Bs around a city, an area or a street address for the dates and guests you choose, with the price of the stay, price per night, discount, review score, stars, room type, distance from your point and free-cancellation and breakfast flags, as JSON or CSV. The code is free and open source (MIT). It runs on the QuanticData Data API, so there are no proxies to rotate and no headless browser to keep alive: sign in once and run a command.

```bash
pip install git+https://github.com/quantumproxies/booking-scraper
booking-scraper login
booking-scraper search "Rome, Italy" --check-in-date 2026-12-01 --check-out-date 2026-12-03 --adults 2 --currency EUR --max-results 100 -o rome.csv
```

`login` opens the QuanticData sign-in page in your browser. New accounts get $2 of free usage every month, no card required: [create one](https://app.quanticdata.io/register?utm_source=github&utm_medium=readme&utm_campaign=booking-scraper).

## What it scrapes

| Command | Input | Returns | Per run |
|---|---|---|---|
| `booking-scraper search` | city, area or street address, dates | Price, discount, distance, badges, review score, 41 fields per row ([fields and price](https://quanticdata.io/collectors/booking-com-scraper-api/?utm_source=github&utm_medium=readme&utm_campaign=booking-scraper)) | up to 100 |

Prices depend on the dates you pass: `--check-in-date` and `--check-out-date` (YYYY-MM-DD) are required, and `price_value` is the price of that stay, `price_per_night` the same divided by the nights. `--adults` and `--rooms` set the party, `--currency` the currency (EUR, USD, NZD...). The place can be a city, an area or a street address, or `--latitude` and `--longitude`; `distance_m` is each property's distance from that point, so an address gives you the properties around one hotel.

## Sample output

A real row from `booking-scraper search "Rome, Italy" --check-in-date 2026-12-01 --check-out-date 2026-12-03 --adults 2 --currency EUR --lang en --max-results 3` (2026-10-23):

```json
{
  "url": "https://www.booking.com/searchresults.html?dest_id=81897&dest_type=hotel&checkin=2026-12-01&checkout=2026-12-03&group_adults=2&no_rooms=1",
  "area": "Trevi, Rome",
  "beds": null,
  "name": "Hotel Castellino Roma",
  "rank": 2,
  "photo": "https://cf.bstatic.com/xdata/images/hotel/square60/323161059.jpg?k=f7ce98368e1232991b02f0e91dba4f0914a77c3f06e3e77155b8e691c492014d&o=",
  "price": "€ 487",
  "stars": 4,
  "nights": 2,
  "photos": [
    "https://cf.bstatic.com/xdata/images/hotel/square60/323161059.jpg?k=f7ce98368e1232991b02f0e91dba4f0914a77c3f06e3e77155b8e691c492014d&o="
  ],
  "country": "it",
  "size_m2": null,
  "bedrooms": null,
  "currency": "EUR",
  "latitude": 41.8968073592107,
  "bathrooms": null,
  "longitude": 12.4823979518605,
  "preferred": true,
  "room_type": "Hotel room: Beds: 1 double or 2 singles",
  "unit_type": "Hotel room",
  "distance_m": 20,
  "photo_large": "https://cf.bstatic.com/xdata/images/hotel/max1024x768/323161059.jpg?k=f7ce98368e1232991b02f0e91dba4f0914a77c3f06e3e77155b8e691c492014d&o=",
  "price_value": 486.5,
  "property_id": 81897,
  "review_word": "Very good",
  "checkin_from": "15:00",
  "discount_pct": 10,
  "review_count": 1703,
  "review_score": 8.5,
  "check_in_date": "2026-12-01",
  "distance_text": "20 m from searched address",
  "quality_class": null,
  "check_out_date": "2026-12-03",
  "checkout_until": "10:30",
  "sustainability": false,
  "taxes_included": false,
  "price_per_night": 243.25,
  "free_cancellation": false,
  "breakfast_included": false,
  "rooms_left_at_price": 4,
  "strikethrough_value": 540.56
}
```

## Python

```python
from quanticdata_booking_scraper import BookingScraper

booking = BookingScraper()  # saved login, or QUANTICDATA_API_KEY

rome = booking.search("Rome, Italy", check_in_date="2026-12-01", check_out_date="2026-12-03",
                      adults=2, currency="EUR", max_results=100)
for p in rome:
    print(p["name"], p["price_per_night"], p["currency"], p["review_score"], p["stars"], p["distance_m"])
rome.to_csv("rome.csv")

deals = [p for p in rome if p["discount_pct"] and p["free_cancellation"]]
print(len(deals), "discounted offers with free cancellation")
```

Each call returns a `Run`: iterate it for the rows (plain dicts), take `len()`, or save it with `to_csv()`, `to_json()`, `to_jsonl()` or `to_dataframe()` (pandas). Errors are specific: `InsufficientCredit`, `RateLimited`, `InvalidInput`, `JobFailed`, `AuthError`.

## Examples

- **Competitive set of a hotel**: Search from your hotel's street address and list the properties within a radius, nearest first, with stars, review score and nightly price for the same night. See [`examples/comp_set.py`](examples/comp_set.py).
- **Rate calendar**: Price the same stay on several check-in dates and get one grid with each property's nightly price per date, the classic rate-shopping sheet. See [`examples/rate_calendar.py`](examples/rate_calendar.py).
- **Deal finder**: Keep the discounted offers of a destination that have free cancellation and a review score above your bar, cheapest per night first. See [`examples/deals.py`](examples/deals.py).

## Command line

Results print as a table; `-o file.csv`, `-o file.json` or `-o file.jsonl` writes a file. List inputs take `a b c`, `a,b,c`, `@file.txt` (one per line) or `-` (stdin). `--no-wait` starts a long run in the background and prints its id; `booking-scraper run <id> -o out.csv` collects it later.

### `booking-scraper search`

Booking.com properties around a place or address for your dates — price, discount, distance, badges, review score.

```
booking-scraper search [LOCATION] [options]
```

| Option | Type | Default | Description |
|---|---|---|---|
| `LOCATION` | string |  | City, area or street address, e.g. "Roma, Italia" or "12 Marine Parade, Napier, New Zealand". Resolved to coordinates first; pass latitude/longitude instead to skip that step. |
| `--latitude` | number |  | Alternative to location. |
| `--longitude` | number |  | Alternative to location. |
| `--check-in-date` | string |  | Check-in date, YYYY-MM-DD. Required. |
| `--check-out-date` | string |  | Check-out date, YYYY-MM-DD (after check-in). Required. |
| `--adults` | integer | `2` | Guests (1-30). |
| `--rooms` | integer | `1` | Rooms (1-10). |
| `--currency` | string |  | Price currency (EUR, USD, NZD...). |
| `--country` | string |  | Country to run the request from, as an ISO 3166-1 alpha-2 code (us, gb, de...). |
| `--lang` | string |  | Interface language, e.g. en, it, de. |
| `--max-results` | integer | `20` | How many properties to deliver at most (1–100). You pay only for delivered properties. |

## Output fields

<details><summary><code>booking-scraper search</code>: 41 fields</summary>

| Field | Type | Description |
|---|---|---|
| `rank` | integer | 1-based position in Booking's order. |
| `name` | string | Property name. |
| `property_id` | integer or null | Booking's own property id. |
| `price` | string or null | Price of the stay as shown on the card. |
| `price_value` | number or null | Numeric price for the whole stay requested; taxes_included says whether taxes and charges are in it. |
| `currency` | string or null | Currency of the price. |
| `strikethrough_value` | number or null | Price before the discount, when Booking shows one. |
| `discount_pct` | integer or null | Discount implied by the two prices. |
| `review_score` | number or null | Guest score out of 10. |
| `review_word` | string or null | Booking's word for that score. |
| `review_count` | integer or null | Number of reviews. |
| `stars` | integer or null | Star class; 0 on apartments and B&Bs that have none. |
| `room_type` | string or null | The unit Booking recommends for this stay. |
| `area` | string or null | Neighbourhood as Booking names it. |
| `distance_m` | integer or null | Metres from the point you searched. |
| `distance_text` | string or null | The distance as Booking phrases it. |
| `free_cancellation` | boolean or null | Booking shows a free-cancellation badge on this offer. |
| `breakfast_included` | boolean or null | Breakfast is included in this price. |
| `rooms_left_at_price` | integer or null | Rooms left at this price, when Booking says so ("we have N left at this price"). |
| `taxes_included` | boolean or null | Whether the price already includes taxes and charges — without it two prices are not comparable. |
| `sustainability` | boolean or null | Property carries a sustainability certification. |
| `preferred` | boolean or null | Booking "Preferred" partner. |
| `quality_class` | integer or null | Booking's own 1-5 quality rating, for properties with no star class. |
| `latitude` | number or null | Property latitude. |
| `longitude` | number or null | Property longitude. |
| `country` | string or null | Country code. |
| `checkin_from` | string or null | Earliest check-in time. |
| `checkout_until` | string or null | Latest check-out time. |
| `photo` | string or null | Main photo URL. |
| `photos` | string[] | Every photo Booking returned for the card. |
| `check_in_date` | string | Echo of the request. |
| `check_out_date` | string | Echo of the request. |
| `nights` | integer or null | Nights of the stay. |
| `price_per_night` | number or null | Stay total divided by the nights. |
| `unit_type` | string or null | Kind of unit from the room label: "Entire apartment", "Private room", "Private suite", "Hotel room"… |
| `size_m2` | number or null | Unit size in m² when the label states it. |
| `beds` | integer or null | Beds in the recommended unit. |
| `bedrooms` | integer or null | Bedrooms, when the label states them. |
| `bathrooms` | integer or null | Bathrooms, when the label states them. |
| `photo_large` | string or null | The main photo at up to 1024×768. |
| `url` | string or null | Link that opens the property on booking.com for the same dates and guests. |

</details>

## Sign-in and API keys

- `booking-scraper login` signs you in with OAuth 2.1 and PKCE in the browser. The token is stored in `~/.config/quanticdata/credentials.json` (readable only by you) and refreshed automatically. One login serves every QuanticData tool on the machine.
- No browser on the machine (SSH, Docker, Colab): run `booking-scraper login --no-browser`, open the link anywhere, then paste back the address the browser ends on.
- Scripts and CI: set `QUANTICDATA_API_KEY` to a key from the dashboard, or store one with `booking-scraper login --api-key`.
- `booking-scraper logout` revokes the token. The connection is listed under API keys in the dashboard as "API · QuanticData CLI"; deleting that key disconnects every machine that uses it.

## Pricing

The code is free and MIT-licensed. Runs are billed to your QuanticData account per delivered row, at the price shown on each collector page linked above; $2 of usage is free every month and failed runs are never billed. Plans with higher limits: [pricing](https://quanticdata.io/pricing/?utm_source=github&utm_medium=readme&utm_campaign=booking-scraper).

## Other ways to call it

The same data over plain HTTP:

```bash
curl -X POST https://api.quanticdata.io/v1/scraper/collectors/booking_stays/run \
  -H "Authorization: Bearer $QUANTICDATA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"input": {"location": "Rome, Italy", "check_in_date": "2026-12-01", "check_out_date": "2026-12-03", "adults": 2, "currency": "EUR", "lang": "en", "max_results": 3}}'
```

- [API reference](https://quanticdata.io/docs/?utm_source=github&utm_medium=readme&utm_campaign=booking-scraper) with Python, Node, PHP and curl examples.
- [MCP server](https://quanticdata.io/mcp-server/?utm_source=github&utm_medium=readme&utm_campaign=booking-scraper) to give Claude, Cursor or any MCP client the same tools.
- [n8n node](https://github.com/quantumproxies/n8n-nodes-quanticdata) for no-code workflows.

## FAQ

**Is this Booking.com scraper free?**

The code is free and MIT-licensed. Scraping runs on your QuanticData account: $2 of usage is free every month with no card, then you pay per delivered row at the price shown on each collector page. Failed runs are never billed.

**Do I need proxies or a headless browser?**

No. You send a place and your dates and get rows back; the requests run on QuanticData's side. It reads public search results only; you are responsible for respecting Booking.com's terms.

**Do the prices depend on the dates?**

Yes. Check-in and check-out are required and every price is for that stay, that party and that currency. Run the same place on other dates, as examples/rate_calendar.py does, to compare.

**How many properties can one run return?**

Up to 100 properties per run; ask for fewer with --max-results and you pay only for what is delivered.

**Can I export to CSV or Excel?**

Add -o properties.csv (or .json, .jsonl). The photo list is joined with '; ', so the CSV opens cleanly in Excel or Google Sheets.

**Can I run it on a schedule?**

Yes. Set QUANTICDATA_API_KEY in the environment and call the CLI or examples/rate_calendar.py from cron, GitHub Actions or any scheduler.

## Related scrapers

- [Google Hotels Scraper](https://github.com/quantumproxies/google-hotels-scraper): Google Hotels scraper for Python and the command line.
- [Airbnb Scraper](https://github.com/quantumproxies/airbnb-scraper): Airbnb scraper for Python and the command line.
- [Google Flights Scraper](https://github.com/quantumproxies/google-flights-scraper): Google Flights scraper for Python and the command line.

## License

MIT. Built and maintained by [QuanticData](https://quanticdata.io/?utm_source=github&utm_medium=readme&utm_campaign=booking-scraper).
