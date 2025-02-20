import logging

from sqlalchemy.orm import Session

from common.models.alert import AlertedListing, UserAlert
from common.schemas.bike_listing import BikeListingBase


def matches_alert(listing: BikeListingBase, alert: UserAlert) -> bool:
    category_match = not alert.category or listing.category == alert.category
    size_match = not alert.size or listing.matches_size(
        alert.size, alert.size_flexibility
    )
    price_match = (
        alert.min_price is not None
        and alert.max_price is not None
        and listing.matches_price_range(alert.min_price, alert.max_price)
    )

    return category_match and size_match and price_match


def has_been_alerted(session: Session, alert_id: int, listing_id: int) -> bool:
    existing = (
        session.query(AlertedListing)
        .filter(
            AlertedListing.alert_id == alert_id, AlertedListing.listing_id == listing_id
        )
        .first()
    )
    # TODO: Check if need to use select() and scalar() instead of first()

    if existing:
        return True

    new_alert = AlertedListing(alert_id=alert_id, listing_id=listing_id)
    session.add(new_alert)
    session.commit()

    return False
