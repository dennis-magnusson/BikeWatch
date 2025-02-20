import argparse
import logging
import os
import traceback
from time import sleep

from db_operations import add_listing
from scraping import find_listings_for_category, scrape_listing
from sqlalchemy.orm import Session
from urls import Category, categories

from common.database import RedisClient, get_db


class Scraper:
    def __init__(
        self,
        session: Session,
        scraping_frequency_minutes: int,
        single_page: bool = False,
    ):
        self.session = session
        self.redis_client = RedisClient()
        self.scraping_frequency_minutes = scraping_frequency_minutes
        self.single_page = single_page

    def scrape_category(self, category: Category):
        logging.info(f"Scraping category ===== {category.name} =====")

        listing_urls: str = find_listings_for_category(
            category, single_page=self.single_page
        )
        logging.debug("Found {} listings".format(len(listing_urls)))

        for url in listing_urls:
            listing = scrape_listing(
                url,
                category_name=category.name,
                session=self.session,
                redis_client=self.redis_client,
            )
            if listing is not None:
                add_listing(self.session, listing)
                logging.debug(f"Listing {listing.id} synced to database")

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
            traceback.print_exc()
        finally:
            logging.info("Closing sqlalchemy session...")
            self.session.close()


def main():
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[logging.FileHandler("scraper.log"), logging.StreamHandler()],
    )

    parser = argparse.ArgumentParser(description="scraper")
    parser.add_argument(
        "--single-page",
        action="store_true",
        help="Scrape only a single page of listings and exit",
    )
    args = parser.parse_args()

    logging.debug(f"Starting scraper, single_page={args.single_page}")

    scraping_frequency_minutes = int(os.environ.get("SCRAPING_FREQUENCY_MINUTES", 60))

    logging.info("Opening sqlalchemy session to sqlite...")
    session = next(get_db())

    scraper = Scraper(session, scraping_frequency_minutes, args.single_page)
    scraper.run()


if __name__ == "__main__":
    main()
