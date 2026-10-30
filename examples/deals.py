"""Discounted Booking.com offers with free cancellation and a good review score.

    python deals.py "Lisbon, Portugal" --check-in 2026-12-01 --check-out 2026-12-03 --min-score 8.5

Reads up to 100 properties for your dates and keeps the ones Booking shows
with a discount, free cancellation and a review score of at least --min-score,
cheapest per night first, with the price before the discount next to it.
"""

import argparse

from quanticdata_booking_scraper import BookingScraper, write

FIELDS = ["name", "area", "review_score", "review_count", "stars", "unit_type", "price_per_night",
          "price_value", "strikethrough_value", "discount_pct", "currency", "breakfast_included",
          "rooms_left_at_price", "url"]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("location")
    parser.add_argument("--check-in", required=True, help="YYYY-MM-DD")
    parser.add_argument("--check-out", required=True, help="YYYY-MM-DD")
    parser.add_argument("--adults", type=int, default=2)
    parser.add_argument("--currency", default="EUR")
    parser.add_argument("--min-score", type=float, default=8.0, help="lowest review score out of 10")
    parser.add_argument("--out", default="deals.csv")
    args = parser.parse_args()

    booking = BookingScraper()
    run = booking.search(args.location, check_in_date=args.check_in, check_out_date=args.check_out,
                         adults=args.adults, currency=args.currency, max_results=100)
    deals = [p for p in run
             if p.get("discount_pct") and p.get("free_cancellation") and p.get("price_per_night")
             and (p.get("review_score") or 0) >= args.min_score]
    deals.sort(key=lambda p: p["price_per_night"])

    for p in deals:
        print(f"{p['price_per_night']:>9,.2f} {p.get('currency') or ''}  -{p['discount_pct']}%  "
              f"{p['review_score']}  {p['name']}")
    write([{k: p.get(k) for k in FIELDS} for p in deals], args.out)
    print(f"{len(deals)} of {len(run)} properties written to {args.out}")


if __name__ == "__main__":
    main()
