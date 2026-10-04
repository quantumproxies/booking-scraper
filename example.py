"""Booking.com scraper API: nightly rates around a place, one typed row per property.

    export QD_API_KEY=...        # https://app.quanticdata.io/register
    python3 example.py "Roma, Italia" 2026-10-16 2026-10-17

Docs and schema: https://quanticdata.io/collectors/booking-com-scraper-api/
"""
import datetime as dt
import os
import sys
import time

import requests

BASE = "https://api.quanticdata.io/v1"
KEY = os.environ.get("QD_API_KEY")
if not KEY:
    sys.exit("Set QD_API_KEY first: https://app.quanticdata.io/register")
HEADERS = {"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"}

today = dt.date.today()
location = sys.argv[1] if len(sys.argv) > 1 else "Roma, Italia"
check_in = sys.argv[2] if len(sys.argv) > 2 else str(today + dt.timedelta(days=14))
check_out = sys.argv[3] if len(sys.argv) > 3 else str(today + dt.timedelta(days=15))

payload = {
    "location": location,
    "check_in_date": check_in,
    "check_out_date": check_out,
    "adults": 2,
    "currency": "EUR",
    "max_results": 20,
}

r = requests.post(f"{BASE}/scraper/collectors/booking_stays/run",
                  headers=HEADERS, json=payload, timeout=180)
body = r.json()
if not r.ok or body.get("type") == "error":
    sys.exit(f"Request failed ({r.status_code}): {body.get('message')}")
run = body["payload"]

# Long runs answer 202 and finish in the background: poll the run until it is done.
while run.get("status") in ("queued", "running"):
    time.sleep(3)
    s = requests.get(f"{BASE}/scraper/collectors/runs/{run['run_id']}",
                     headers=HEADERS, timeout=60)
    run = s.json()["payload"]

rows = run.get("results") or []
for row in rows:
    was = f"  (was {row['strikethrough_value']}, -{row['discount_pct']}%)" if row.get("discount_pct") else ""
    print(f"{row['rank']:>3}  {row['price_value']:>8} {row['currency']}  "
          f"{row.get('review_score') or '-':>4}  {row['name']}{was}")
print(f"{len(rows)} properties for {check_in} to {check_out}")
