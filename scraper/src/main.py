import logging
import os
from time import sleep
from typing import Iterable

from db_operations import sync_listings
from scraping import find_listings_for_category, scrape_listing
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from urls import Category, categories

from common.models import Base, BikeListingData


class Scraper:
    def __init__(
        self,
        session: Session,
        scraping_frequency_minutes: int,
        scraping_page_limit: int,
    ):
        self.session = session
        self.scraping_frequency_minutes = scraping_frequency_minutes
        self.scraping_page_limit = scraping_page_limit

    def scrape_category(self, category: Category):
        logging.info(f"Scraping category ===== {category.name} =====")

        listing_urls: str = find_listings_for_category(category)
        logging.debug("Found {} listings".format(len(listing_urls)))

        listings: Iterable[BikeListingData] = [
            scrape_listing(listing, category_name=category.name)
            for listing in listing_urls
        ]
        logging.debug("Scraped {} listings".format(len(listings)))

        sync_listings(self.session, listings)
        logging.info("Listings synced to database")

    def run(self):
        try:
            while True:
                logging.info("Scraping cycle started")
                for category in categories:
                    self.scrape_category(category)
                logging.info(
                    "Scraping cycle completed, sleeping for {} minutes".format(
                        self.scraping_frequency_minutes
                    )
                )
                sleep(self.scraping_frequency_minutes * 60)
        except Exception as e:
            logging.error(f"An error occurred: {e}")
        finally:
            logging.info("Closing sqlalchemy session...")
            self.session.close()


def main():
    logging.basicConfig(
        level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
    )

    scraping_frequency_minutes = int(os.environ.get("SCRAPING_FREQUENCY_MINUTES", 60))
    scraping_page_limit = int(os.environ.get("PAGE_COUNT", 50))

    logging.info("Opening sqlalchemy session to sqlite...")
    engine = create_engine("sqlite:///data/bikes.db")
    Session = sessionmaker(bind=engine)
    session = Session()

    logging.info("Database connected")

    Base.metadata.drop_all(engine)
    logging.info("Database schema dropped")
    Base.metadata.create_all(engine)
    logging.info("Database schema created")

    scraper = Scraper(session, scraping_frequency_minutes, scraping_page_limit)
    scraper.run()


if __name__ == "__main__":
    main()
