import logging
from typing import Iterable

from common.models import BikeImage, BikeListing
from common.schemas.bike_listing import BikeListingBase


def sync_listings(session, scraped_data: Iterable[BikeListingBase]):
    existing_bike_ids = {bike.id for bike in session.query(BikeListing.id).all()}

    for item in scraped_data:
        if item.id not in existing_bike_ids:
            add_listing(session, item)
        else:
            logging.info(f"Bike with ID {item.id} already exists. Skipping.")


def add_listing(session, listing: BikeListingBase):
    bike = BikeListing(
        id=listing.id,
        title=listing.title,
        brand=listing.brand,
        model=listing.model,
        year=listing.year,
        url=listing.url,
        date_posted=listing.date_posted,
        letter_size_min=listing.letter_size_min,
        letter_size_max=listing.letter_size_max,
        number_size_min=listing.number_size_min,
        number_size_max=listing.number_size_max,
        price=listing.price,
        city=listing.city,
        region=listing.region,
        description=listing.description,
        short_description=listing.short_description,
        category=listing.category,
    )

    for image_url in listing.images:
        bike.images.append(BikeImage(image_url=image_url))

    session.add(bike)
    session.commit()
