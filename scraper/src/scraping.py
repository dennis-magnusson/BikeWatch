import logging
from typing import List

from bs4 import BeautifulSoup
from parsing import (
    parse_date_posted,
    parse_raw_description,
    parse_raw_images,
    parse_raw_title,
)
from request_throttler import get_request
from urls import Category, get_url

from common.models import BikeListingData

logger = logging.getLogger(__name__)


def get_category_page_count(base_url: str) -> int:
    url = base_url.format(1)

    response = get_request(url)
    soup = BeautifulSoup(response.text, "html.parser")
    last_page = soup.find("a", class_="ipsPagination_last").get("data-page")

    return int(last_page)


def find_listings_for_category(category: Category) -> List[str]:
    base_url = get_url(category)
    pages = get_category_page_count(base_url)
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
    return url.rstrip("/").split("/")[-1]


def scrape_listing(url: str, category_name: str) -> BikeListingData:
    response = get_request(url)
    soup = BeautifulSoup(response.text, "html.parser")

    id = get_listing_id(url)
    title = parse_raw_title(soup, category_name)
    date_posted = parse_date_posted(soup)
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

    return BikeListingData(
        id=id,
        title=title,
        brand=brand,
        model=model,
        year=year,
        url=url,
        date_posted=date_posted,
        number_size_min=number_size_min,
        number_size_max=number_size_max,
        letter_size_min=letter_size_min,
        letter_size_max=letter_size_max,
        images=images,
        price=price,
        city=city,
        region=region,
        description=description,
        short_description=short_description,
        category=category_name,
    )
