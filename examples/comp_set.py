"""The Booking.com properties around one address, nearest first.

    python comp_set.py "12 Marine Parade, Napier, New Zealand" --check-in 2026-12-01 --check-out 2026-12-03 --currency NZD --radius 1500

Searches from a street address (your hotel's, for example), keeps the
properties within --radius metres and writes them nearest first with stars,
review score, unit type, nightly price, discount and free-cancellation flag.
It prints the median nightly price of the set: what the properties next door
charge for the same night.
"""

import argparse
from statistics import median

from quanticdata_booking_scraper import BookingScraper, write

FIELDS = ["distance_m", "name", "stars", "quality_class", "review_score", "review_count", "unit_type",
          "price_per_night", "price_value", "currency", "discount_pct", "free_cancellation",
          "breakfast_included", "taxes_included", "url"]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("address", help="street address, area or city")
    parser.add_argument("--check-in", required=True, help="YYYY-MM-DD")
    parser.add_argument("--check-out", required=True, help="YYYY-MM-DD")
    parser.add_argument("--adults", type=int, default=2)
    parser.add_argument("--currency", default="EUR")
    parser.add_argument("--radius", type=int, default=1000, help="metres from the address")
    parser.add_argument("--max-results", type=int, default=100, help="properties to read (max 100)")
    parser.add_argument("--out", default="comp_set.csv")
    args = parser.parse_args()

    booking = BookingScraper()
    run = booking.search(args.address, check_in_date=args.check_in, check_out_date=args.check_out,
                         adults=args.adults, currency=args.currency, max_results=args.max_results)
    near = [p for p in run if p.get("distance_m") is not None and p["distance_m"] <= args.radius]
    near.sort(key=lambda p: p["distance_m"])

    rows = [{k: p.get(k) for k in FIELDS} for p in near]
    nightly = [p["price_per_night"] for p in near if p.get("price_per_night")]
    for p in near:
        print(f"{p['distance_m']:>6} m  {str(p.get('stars') or '-'):>2}*  {str(p.get('review_score') or '-'):>4}  "
              f"{p.get('price_per_night')} {p.get('currency') or ''}  {p['name']}")
    if nightly:
        print(f"median nightly price within {args.radius} m: {median(nightly):,.2f} {args.currency}")
    write(rows, args.out)
    print(f"{len(rows)} properties written to {args.out}")


if __name__ == "__main__":
    main()
