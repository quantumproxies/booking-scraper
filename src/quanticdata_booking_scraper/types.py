"""Row types of each command, for editors and type checkers (rows are plain dicts)."""

from typing import Any, Dict, List, Optional

try:  # Python 3.8+
    from typing import TypedDict
except ImportError:  # pragma: no cover
    from typing_extensions import TypedDict  # type: ignore


class BookingStaysRow(TypedDict, total=False):
    """One row of `booking-scraper search` (booking_stays v1.2.1)."""

    rank: int
    """1-based position in Booking's order."""
    name: str
    """Property name."""
    property_id: Optional[int]
    """Booking's own property id."""
    price: Optional[str]
    """Price of the stay as shown on the card."""
    price_value: Optional[float]
    """Numeric price for the whole stay requested; taxes_included says whether taxes and charges are in it."""
    currency: Optional[str]
    """Currency of the price."""
    strikethrough_value: Optional[float]
    """Price before the discount, when Booking shows one."""
    discount_pct: Optional[int]
    """Discount implied by the two prices."""
    review_score: Optional[float]
    """Guest score out of 10."""
    review_word: Optional[str]
    """Booking's word for that score."""
    review_count: Optional[int]
    """Number of reviews."""
    stars: Optional[int]
    """Star class; 0 on apartments and B&Bs that have none."""
    room_type: Optional[str]
    """The unit Booking recommends for this stay."""
    area: Optional[str]
    """Neighbourhood as Booking names it."""
    distance_m: Optional[int]
    """Metres from the point you searched."""
    distance_text: Optional[str]
    """The distance as Booking phrases it."""
    free_cancellation: Optional[bool]
    """Booking shows a free-cancellation badge on this offer."""
    breakfast_included: Optional[bool]
    """Breakfast is included in this price."""
    rooms_left_at_price: Optional[int]
    """Rooms left at this price, when Booking says so ("we have N left at this price")."""
    taxes_included: Optional[bool]
    """Whether the price already includes taxes and charges — without it two prices are not comparable."""
    sustainability: Optional[bool]
    """Property carries a sustainability certification."""
    preferred: Optional[bool]
    """Booking "Preferred" partner."""
    quality_class: Optional[int]
    """Booking's own 1-5 quality rating, for properties with no star class."""
    latitude: Optional[float]
    """Property latitude."""
    longitude: Optional[float]
    """Property longitude."""
    country: Optional[str]
    """Country code."""
    checkin_from: Optional[str]
    """Earliest check-in time."""
    checkout_until: Optional[str]
    """Latest check-out time."""
    photo: Optional[str]
    """Main photo URL."""
    photos: List[str]
    """Every photo Booking returned for the card."""
    check_in_date: str
    """Echo of the request."""
    check_out_date: str
    """Echo of the request."""
    nights: Optional[int]
    """Nights of the stay."""
    price_per_night: Optional[float]
    """Stay total divided by the nights."""
    unit_type: Optional[str]
    """Kind of unit from the room label: "Entire apartment", "Private room", "Private suite", "Hotel room"…"""
    size_m2: Optional[float]
    """Unit size in m² when the label states it."""
    beds: Optional[int]
    """Beds in the recommended unit."""
    bedrooms: Optional[int]
    """Bedrooms, when the label states them."""
    bathrooms: Optional[int]
    """Bathrooms, when the label states them."""
    photo_large: Optional[str]
    """The main photo at up to 1024×768."""
    url: Optional[str]
    """Link that opens the property on booking.com for the same dates and guests."""
