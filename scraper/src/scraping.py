import logging
import re
from typing import List, Optional

from bs4 import BeautifulSoup
from parsing import (
    parse_date_posted,
    parse_raw_description,
    parse_raw_images,
    parse_raw_title,
    sold_keywords,
)
from request_throttler import get_request
from urls import Category, get_url

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


def scrape_listing(url: str, category_name: str) -> Optional[BikeListingBase]:
    response = get_request(url)
    soup = BeautifulSoup(response.text, "html.parser")

    id = get_listing_id(url)
    title = parse_raw_title(soup, category_name)
    date_posted = parse_date_posted(soup)

    most_likely_sold = any(keyword in title.lower() for keyword in sold_keywords)
    too_old = False  # TODO: Implement this
    if most_likely_sold or too_old:
        return None

    (
        brand,
        model,
        price,
        year,
        number_size_min,
        number_size_max,
        letter_size_min,
        letter_size_max,
        region,
        city,
        description,
        short_description,
    ) = parse_raw_description(soup)
    images = parse_raw_images(soup)

    return BikeListingBase(
        id=id,
        title=title,
        brand=brand,
        model=model,
        year=year,
        url=url,
        date_posted=date_posted,
        number_size_min=number_size_min,
        number_size_max=number_size_max,
        letter_size_min=letter_size_min.value if letter_size_min else None,
        letter_size_max=letter_size_max.value if letter_size_max else None,
        price=price,
        city=city,
        region=region,
        description=description,
        short_description=short_description,
        images=images,
        category=category_name,
    )
