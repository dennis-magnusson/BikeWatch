from typing import Iterable

from data.models import BikeImage, BikeListing, BikeListingData


def sync_listings(session, scraped_data: Iterable[BikeListingData]):
    existing_bike_ids = {bike.id for bike in session.query(BikeListing.id).all()}

    for item in scraped_data:
        if item.id not in existing_bike_ids:
            add_listing(session, item)
        else:
            print(f"Bike with ID {item.id} already exists. Skipping.")


def add_listing(session, listing_data: BikeListingData):
    bike = BikeListing(
        id=listing_data.id,
        title=listing_data.title,
        brand=listing_data.brand,
        model=listing_data.model,
        year=listing_data.year,
        url=listing_data.url,
        date_posted=listing_data.date_posted,
        size=listing_data.size,
        price=listing_data.price,
        city=listing_data.city,
        region=listing_data.region,
        description=listing_data.description,
        short_description=listing_data.short_description,
    )

    for image_url in listing_data.images:
        bike.images.append(BikeImage(image_url=image_url))

    session.add(bike)
    session.commit()
