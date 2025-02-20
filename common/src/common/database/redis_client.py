import json

import redis

from common.schemas.bike_listing import BikeListingBase


class RedisClient:
    def __init__(self, host: str = "redis", port: int = 6379):
        self.redis = redis.Redis(host=host, port=port, decode_responses=True)
        self.channel = "bike_alerts"

    def publish_alert(self, chat_id: int, listing: BikeListingBase) -> None:
        message = {"chat_id": chat_id, "listing": listing.dict()}
        self.redis.publish(self.channel, json.dumps(message))

    def subscribe_to_alerts(self):
        pubsub = self.redis.pubsub()
        pubsub.subscribe(self.channel)
        return pubsub
