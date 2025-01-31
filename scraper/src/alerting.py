import logging
import os

import requests
from sqlalchemy.orm import Session

from common.models.alert import UserAlert
from common.schemas.bike_listing import BikeListingBase

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


def send_telegram_message(chat_id: str, message: str):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
    }
    response = requests.post(url, json=payload)
    logging.debug(f"Telegram message sent. Response: {response.text}")
    response.raise_for_status()


def matches_alert(listing: BikeListingBase, alert: UserAlert) -> bool:
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
