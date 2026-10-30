"""Booking.com Scraper: Booking scraper for Python and the command line: Booking.com hotels and apartments around a city or street address for your dates, with stay price, price per night, discount, review score, stars, distance and free-cancellation flag, as JSON or CSV. Free and open source; sign in with your QuanticData account, no proxies or headless browser to run.

    from quanticdata_booking_scraper import BookingScraper

    scraper = BookingScraper()   # saved login (`booking-scraper login`) or QUANTICDATA_API_KEY
    run = scraper.search(...)   # Booking.com properties around a place or address for your dates
"""

from typing import Any, Dict, Optional, Sequence, Union

from ._qd.client import Client, Run
from ._qd.errors import (APIError, AuthError, InsufficientCredit, InvalidInput, JobFailed, JobTimeout,
                         QuanticDataError, RateLimited)
from ._qd.output import write

__version__ = "0.1.0"
__all__ = ["BookingScraper", "Run", "write", "APIError", "AuthError", "InsufficientCredit", "InvalidInput",
           "JobFailed", "JobTimeout", "QuanticDataError", "RateLimited", "__version__"]


def _as_list(value: Any) -> Any:
    if value is None or isinstance(value, (list, tuple)):
        return list(value) if value is not None else None
    return [value]


class BookingScraper:
    """Booking.com Scraper on the QuanticData Data API.

    Every method runs one collector and returns a :class:`Run`: iterate it for the
    rows (plain dicts, typed in ``types``), or save it with ``to_csv()``,
    ``to_json()``, ``to_jsonl()`` or ``to_dataframe()``.
    """

    def __init__(self, api_key: Optional[str] = None, *, timeout: float = 180.0) -> None:
        self.client = Client(api_key, user_agent="booking-scraper/0.1.0 (+https://github.com/quantumproxies/booking-scraper)", timeout=timeout)

    def search(
        self, location: Optional[str] = None,
        *,
        check_in_date: str,
        check_out_date: str,
        latitude: Optional[float] = None,
        longitude: Optional[float] = None,
        adults: Optional[int] = None,
        rooms: Optional[int] = None,
        currency: Optional[str] = None,
        country: Optional[str] = None,
        lang: Optional[str] = None,
        max_results: Optional[int] = None,
        wait: bool = True,
        timeout: float = 900.0,
    ) -> Run:
        """Booking.com properties around a place or address for your dates — price, discount, distance, badges, review score.

        Args:
            location: City, area or street address, e.g. "Roma, Italia" or "12 Marine Parade, Napier, New Zealand". Resolved to coordinates first; pass latitude/longitude instead to skip that step.
            latitude: Alternative to location.
            longitude: Alternative to location.
            check_in_date: Check-in date, YYYY-MM-DD.
            check_out_date: Check-out date, YYYY-MM-DD (after check-in).
            adults: Guests (1-30).
            rooms: Rooms (1-10).
            currency: Price currency (EUR, USD, NZD...).
            country: Country to run the request from, as an ISO 3166-1 alpha-2 code (us, gb, de...).
            lang: Interface language, e.g. en, it, de.
            max_results: How many properties to deliver at most (1–100). You pay only for delivered properties.
            wait: False starts the run in the background and returns its id at once.
            timeout: seconds to wait for a background run before giving up.

        Returns up to 100 rows, one per property: see ``types.BookingStaysRow``.
        """
        payload = {
            "location": location,
            "latitude": latitude,
            "longitude": longitude,
            "check_in_date": check_in_date,
            "check_out_date": check_out_date,
            "adults": adults,
            "rooms": rooms,
            "currency": currency,
            "country": country,
            "lang": lang,
            "max_results": max_results,
        }
        return self.client.run_collector("booking_stays", payload, wait=wait, timeout=timeout)
