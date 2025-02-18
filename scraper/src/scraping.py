import logging
import re
from dataclasses import asdict
from typing import List, Optional

from alerting import (
    has_been_alerted,
    matches_alert,
    send_new_listing_notification_telegram,
)
from bs4 import BeautifulSoup
from parsing import (
    ParsedListingData,
    parse_date_posted,
    parse_raw_description,
    parse_raw_images,
    parse_raw_title,
    sold_keywords,
)
from request_throttler import get_request
from sqlalchemy.orm import Session
from urls import Category, get_url

from common.models.alert import AlertedListing, UserAlert
from common.schemas.bike_listing import BikeListingBase

logger = logging.getLogger(__name__)


def get_category_page_count(base_url: str) -> int:
    url = base_url.format(1)
    logger.debug(f"Getting page count for category {url!r}")
    response = get_request(url)
    soup = BeautifulSoup(response.text, "html.parser")

    last_page_li = soup.find("li", class_="ipsPagination_last")
    last_page_anchor = last_page_li.find("a")
    if last_page_anchor:
        return int(last_page_anchor.get("data-page"))
    else:
        raise ValueError("Could not find last page anchor")


def find_listings_for_category(category: Category, single_page: bool) -> List[str]:
    base_url = get_url(category)
    pages = 1 if single_page else get_category_page_count(base_url)
    logger.info(f"Found {pages} pages for category {category.name}")
    urls = [base_url.format(page) for page in range(1, pages + 1)]

    found_listings = []

    for url in urls:
        response = get_request(url)
        soup = BeautifulSoup(response.text, "html.parser")

        ol = soup.find("ol", class_="ipsDataList")
        listings = ol.find_all("h4")

        found_listings.extend(
            [
                listing.find_all("a")[1].get("href")
                for listing in listings
                if len(listing.find_all("a")) >= 2
            ]
        )

    return found_listings


def get_listing_id(url: str) -> str:
    # TODO: Make sure this is robust and truly unique
    id_digits = re.findall(r"\d+", url)
    if id_digits:
        return id_digits[0]
    else:
        logging.error(f"Could not find id for url {url}")
        parts = url.rstrip("/").split("/")
        return parts[-1] if parts[-1][0] != "#" else parts[-2]


def scrape_listing(
    url: str, category_name: str, session: Session
) -> Optional[BikeListingBase]:
    response = get_request(url)
    soup = BeautifulSoup(response.text, "html.parser")

    id = get_listing_id(url)
    title = parse_raw_title(soup, category_name)
    date_posted, too_old = parse_date_posted(soup, max_age_months=15)

    most_likely_sold = any(keyword in title.lower() for keyword in sold_keywords)
    # check that listing was not posted more than 15 months ago
    if most_likely_sold or too_old:
        logging.info(f"Sold or too old: {url=}, {most_likely_sold=}, {too_old=}")
        return None

    parsed_data: ParsedListingData = parse_raw_description(soup)
    images = parse_raw_images(soup)

    listing = BikeListingBase(
        id=id,
        title=title,
        url=url,
        date_posted=date_posted,
        category=category_name,
        images=images,
        **asdict(parsed_data),
    )

    # Check alerts and send notifications
    alerts = session.query(UserAlert).all()
    for alert in alerts:
        if matches_alert(listing, alert) and not has_been_alerted(
            session, alert.id, listing.id
        ):
            send_new_listing_notification_telegram(
                alert.chat_id,
                listing,
            )
            alerted_listing = AlertedListing(alert_id=alert.id, listing_id=listing.id)
            session.add(alerted_listing)
            session.commit()

    return listing
