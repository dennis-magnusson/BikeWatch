import logging
import os

import requests
from sqlalchemy.orm import Session

from common.models.alert import AlertedListing, UserAlert
from common.schemas.bike_listing import BikeListingBase

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


def send_new_listing_notification_telegram(chat_id: str, listing: BikeListingBase):
    try:
        size = listing.size_as_string() if listing is not None else None
        message = (
            f"<b>{listing.title}</b>\n"
            f"🚴 Category: {listing.category.capitalize()}\n"
            f"💶 Price: <strong>{int(listing.price)}€</strong>\n"
            f"📏 Size: {size}\n"
            f"📍 {listing.city}, {listing.region}\n\n"
            f"<a href='{listing.url}'>🔗 View</a>"
        )

        if listing.images:
            # Try sending with photo first
            try:
                url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
                payload = {
                    "chat_id": chat_id,
                    "photo": listing.images[0],
                    "caption": message,
                    "parse_mode": "HTML",
                }
                response = requests.post(url, json=payload)
                response.raise_for_status()
                return
            except requests.exceptions.RequestException as e:
                logging.warning(
                    f"Failed to send photo message: {e}. Falling back to text-only message"
                )

        # If no images or photo send failed, send text-only message
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": message,
            "parse_mode": "HTML",
        }
        response = requests.post(url, json=payload)
        response.raise_for_status()

    except Exception as e:
        logging.error(f"Failed to send Telegram notification: {e}")


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

    logging.info(
        f"Checking if alert {alert_id} has been alerted for listing {listing_id}"
    )
    logging.info(f"Existing alert: {existing}")

    if existing:
        return True

    new_alert = AlertedListing(alert_id=alert_id, listing_id=listing_id)
    session.add(new_alert)
    session.commit()

    return False
