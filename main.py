import json
from typing import Iterable

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from data.models import Base, BikeListingData
from scraper.scraper import find_listings_for_category, scrape_listing
from utils.db_operations import add_listing, sync_listings

print("Opening sqlalchemy session to sqlite...")
engine = create_engine("sqlite:///bikes.db")

Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

url = "https://www.fillaritori.com/forum/54-maantie/?filterByState=8"
listing_urls = find_listings_for_category(url)

# listing_urls = listing_urls[0:2]

listings: Iterable[BikeListingData] = [
    scrape_listing(listing) for listing in listing_urls
]

sync_listings(session, listings)

print("Closing session")
session.close()
