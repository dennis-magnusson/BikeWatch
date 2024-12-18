import logging
import os
from time import sleep
from typing import Iterable

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from data.models import Base, BikeListingData
from scraping.scraper import find_listings_for_category, scrape_listing
from utils.db_operations import sync_listings


def main():

    logging.basicConfig(
        level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
    )

    scraping_frequency = int(os.environ.get("SCRAPING_FREQUENCY_MINUTES", 60))
    base_url = "https://www.fillaritori.com/forum/54-maantie/page/{}/?filterByState=8"

    logging.info("Opening sqlalchemy session to sqlite...")
    engine = create_engine("sqlite:///data/bikes.db")
    Session = sessionmaker(bind=engine)
    session = Session()

    logging.info("Database connected")

    # Base.metadata.drop_all(engine)
    # Base.metadata.create_all(engine)

    try:
        while True:
            logging.info("Scraping cycle started")

            listing_urls = find_listings_for_category(base_url, pages=8)
            logging.debug("Found {} listings".format(len(listing_urls)))

            listings: Iterable[BikeListingData] = [
                scrape_listing(listing) for listing in listing_urls
            ]
            logging.debug("Scraped {} listings".format(len(listings)))

            sync_listings(session, listings)
            logging.info("Listings synced to database")

            logging.info(
                "Scraping cycle completed, sleeping for {} minutes".format(
                    scraping_frequency
                )
            )
            sleep(scraping_frequency * 60)
    except Exception as e:
        logging.error(f"An error occurred: {e}")
    finally:
        logging.info("Closing sqlalchemy session...")
        session.close()


if __name__ == "__main__":
    main()
