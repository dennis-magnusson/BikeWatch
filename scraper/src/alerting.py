import logging
import os

import requests
from sqlalchemy.orm import Session

from common.models.alert import UserAlert
from common.schemas.bike_listing import BikeListingBase

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


def _format_size_string(listing: BikeListingBase) -> str:
    if listing.letter_size_max and listing.letter_size_min:
        if listing.letter_size_max == listing.letter_size_min:
            return listing.letter_size_max
        else:
            return f"{listing.letter_size_min} - {listing.letter_size_max}"
    elif listing.letter_size_min and listing.letter_size_max:
        if listing.letter_size_min == listing.letter_size_max:
            return listing.letter_size_min
        else:
            return f"{listing.letter_size_min} - {listing.letter_size_max}"
    else:
        return "N/A"


def send_new_listing_notification_telegram(chat_id: str, listing: BikeListingBase):
    try:
        size = _format_size_string(listing)
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
    category_match = alert.category and listing.category == alert.category
    size_match = alert.size and listing.matches_size(alert.size, alert.size_flexibility)
    price_match = (
        alert.min_price
        and alert.max_price
        and listing.matches_price_range(alert.min_price, alert.max_price)
    )
    return category_match and size_match and price_match


def has_been_alerted(session: Session, alert_id: int, listing_id: int) -> bool:
    # TODO: Implement this
    return False
