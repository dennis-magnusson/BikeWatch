import asyncio
import json
import logging

from common.database import RedisClient, get_db
from common.models.bike_listing import BikeListing
from common.schemas.bike_listing import BikeListingBase


class AlertListener:
    def __init__(self, bot):
        self.redis_client = RedisClient()
        self.bot = bot
        self.db_session = next(get_db())

    async def start_listening(self):
        pubsub = self.redis_client.subscribe_to_alerts()

        while True:
            message = pubsub.get_message()
            if message and message["type"] == "message":
                data = json.loads(message["data"])
                chat_id: str = data["chat_id"]
                listing_data: dict = data["listing"]

                try:
                    listing = BikeListingBase.model_validate(listing_data)
                    await self._send_alert_message(chat_id, listing)
                except ValueError as e:
                    logging.warning(
                        f"Invalid listing data in alert message {message=}: {e}"
                    )
                    continue

            await asyncio.sleep(0.1)

    async def _send_alert_message(self, chat_id: str, listing: BikeListingBase):
        size = listing.size_as_string()
        message = (
            f"<b>{listing.title}</b>\n"
            f"🚴 Category: {listing.category.capitalize()}\n"
            f"💶 Price: <strong>{int(listing.price)}€</strong>\n"
            f"📏 Size: {size}\n"
            f"📍 {listing.city}, {listing.region}\n\n"
            f"<a href='{listing.url}'>🔗 View</a>"
        )

        if listing.images:
            await self.bot.send_photo(
                chat_id, listing.images[0], caption=message, parse_mode="HTML"
            )
        else:
            await self.bot.send_message(chat_id, message, parse_mode="HTML")
