import re

import requests
from bs4 import BeautifulSoup

from data.models import BikeListing, BikeListingData
from scraper.parsing import (
    parse_date_posted,
    parse_raw_description,
    parse_raw_images,
    parse_raw_title,
)
from scraper.request_throttler import get_request


def find_listings_for_category(url):
    response = get_request(url)

    soup = BeautifulSoup(response.text, "html.parser")

    ol = soup.find("ol", class_="ipsDataList")
    listings = ol.find_all("h4")

    found_listings = [listing.find_all("a")[1]["href"] for listing in listings]

    return found_listings


def get_listing_id(url: str) -> str:
    return url.rstrip("/").split("/")[-1]


def scrape_listing(url: str) -> BikeListingData:
    response = get_request(url)
    soup = BeautifulSoup(response.text, "html.parser")

    id = get_listing_id(url)
    title = parse_raw_title(soup)
    date_posted = parse_date_posted(soup)
    brand, model, price, year, size, region, city, description, short_description = (
        parse_raw_description(soup)
    )
    images = parse_raw_images(soup)

    return BikeListingData(
        id=id,
        title=title,
        brand=brand,
        model=model,
        year=year,
        url=url,
        date_posted=date_posted,
        size=size,
        images=images,
        price=price,
        city=city,
        region=region,
        description=description,
        short_description=short_description,
    )
