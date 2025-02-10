import logging

from common.models import BikeImage, BikeListing
from common.schemas.bike_listing import BikeListingBase


def add_listing(session, listing: BikeListingBase):
    existing_bike = (
        session.query(BikeListing).filter(BikeListing.id == listing.id).first()
    )

    # TODO: Check if the listing has had a price change and update + alert user

    if existing_bike:
        logging.info(f"Bike with ID {listing.id} already exists. Skipping.")
        return

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
        category=listing.category,
    )

    for image_url in listing.images:
        bike.images.append(BikeImage(image_url=image_url))

    session.add(bike)
    session.commit()
