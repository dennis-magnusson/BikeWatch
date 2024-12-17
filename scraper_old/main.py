import json
from typing import Iterable
import sys

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from data.models import Base, BikeListingData
from scraping.scraper import find_listings_for_category, scrape_listing
from utils.db_operations import add_listing, sync_listings


def main():
    # if argument from_empty is given, then we will start from an empty database

    print("Opening sqlalchemy session to sqlite...")
    engine = create_engine("sqlite:///bikes.db")

    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    base_url = "https://www.fillaritori.com/forum/54-maantie/page/{}/?filterByState=8"
    listing_urls = find_listings_for_category(base_url, pages=8)

    print("Found {} listings".format(len(listing_urls)))
    print("Beginning to scrape ...")

    listings: Iterable[BikeListingData] = [
        scrape_listing(listing) for listing in listing_urls
    ]

    sync_listings(session, listings)

    print("Closing session")
    session.close()


if __name__ == "__main__":
    main()
