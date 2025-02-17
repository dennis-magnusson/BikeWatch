import logging
import os

import requests
from sqlalchemy.orm import Session

from common.models.alert import UserAlert
from common.schemas.bike_listing import BikeListingBase

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


# TODO: Move this to a better place (maybe common package)
def format_size_string(listing: BikeListingBase) -> str:
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
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"

    size = format_size_string(listing)

    message = (
        f"<b>{listing.title}</b>\n"
        f"💰 Price: <strong>{int(listing.price)}€</strong>\n"
        f"📏 Size: {size}\n"
        f"📍 Location: {listing.city}, {listing.region}\n\n"
        f"<a href='{listing.url}'>🔗 View Listing</a>"
    )

    payload = {
        "chat_id": chat_id,
        "photo": listing.images[0],
        "caption": message,
        "parse_mode": "HTML",
    }

    response = requests.post(url, json=payload)
    logging.debug(f"Telegram message sent. Response: {response.text}")
    response.raise_for_status()


def matches_alert(listing: BikeListingBase, alert: UserAlert) -> bool:
    # TODO: Handle missing values in listing
    if alert.min_price and listing.price < alert.min_price:
        return False
    if alert.max_price and listing.price > alert.max_price:
        return False
    if alert.category and listing.category != alert.category:
        return False
    if alert.city and listing.city != alert.city:
        return False
    if alert.region and listing.region != alert.region:
        return False
    if alert.size and listing.number_size_max and listing.number_size_min:
        max_size = alert.size + 1 if alert.size_flexibility else alert.size
        min_size = alert.size - 1 if alert.size_flexibility else alert.size
        if listing.number_size_max >= max_size or listing.number_size_min <= min_size:
            return False
    return True


def has_been_alerted(session: Session, alert_id: int, listing_id: int) -> bool:
    # TODO: Implement this
    return False
