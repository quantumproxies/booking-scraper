"""Booking.com rate calendar: each property's nightly price across check-in dates.

    python rate_calendar.py "Rome, Italy" --start 2026-12-01 --dates 5 --step 7 --nights 2 --currency EUR

Prices the same stay on --dates check-in dates, --step days apart, and writes
one row per property with its nightly price on each date (empty when Booking
does not offer it that night). Properties are matched across dates by their
Booking id. This is the rate-shopping grid revenue managers keep for a market.
"""

import argparse
from datetime import date, timedelta

from quanticdata_booking_scraper import BookingScraper, write


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("location", help="city, area or street address")
    parser.add_argument("--start", required=True, help="first check-in date, YYYY-MM-DD")
    parser.add_argument("--dates", type=int, default=5, help="how many check-in dates to price")
    parser.add_argument("--step", type=int, default=7, help="days between check-in dates")
    parser.add_argument("--nights", type=int, default=2)
    parser.add_argument("--adults", type=int, default=2)
    parser.add_argument("--currency", default="EUR")
    parser.add_argument("--max-results", type=int, default=50, help="properties per date (max 100)")
    parser.add_argument("--out", default="rate_calendar.csv")
    args = parser.parse_args()

    booking = BookingScraper()
    start = date.fromisoformat(args.start)
    grid = {}
    columns = []
    for i in range(args.dates):
        check_in = start + timedelta(days=i * args.step)
        check_out = check_in + timedelta(days=args.nights)
        column = check_in.isoformat()
        columns.append(column)
        run = booking.search(args.location, check_in_date=column, check_out_date=check_out.isoformat(),
                             adults=args.adults, currency=args.currency, max_results=args.max_results)
        for p in run:
            key = p.get("property_id") or p["name"]
            row = grid.setdefault(key, {"property_id": p.get("property_id"), "name": p["name"],
                                        "stars": p.get("stars"), "review_score": p.get("review_score"),
                                        "area": p.get("area")})
            row[column] = p.get("price_per_night")
        print(f"{column}: {len(run)} properties priced")

    rows = [{**r, **{c: r.get(c) for c in columns}} for r in grid.values()]
    write(rows, args.out)
    print(f"{len(rows)} properties x {len(columns)} dates written to {args.out}")


if __name__ == "__main__":
    main()
