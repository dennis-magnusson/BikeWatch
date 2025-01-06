from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel
from sqlalchemy import DateTime, ForeignKey, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class BikeListingBase(BaseModel):
    id: Optional[str] = None
    title: str
    brand: Optional[str] = None
    model: Optional[str] = None
    year: Optional[int] = None
    url: str
    date_posted: Optional[str] = None
    size: Optional[str] = None
    price: Optional[float] = None
    city: Optional[str] = None
    region: Optional[str] = None
    description: Optional[str] = None
    short_description: Optional[str] = None
    images: List[str] = []

    class Config:
        orm_mode = True


class BikeListingRead(BikeListingBase):
    id: str
    date_first_seen: datetime
    date_last_updated: datetime


class Base(DeclarativeBase):
    pass


class BikeListingData:
    def __init__(
        self,
        id,
        title,
        brand,
        model,
        year,
        url,
        date_posted,
        size,
        images,
        price,
        city,
        region,
        description,
        short_description,
    ):

        self.id = id
        self.title = title
        self.brand = brand
        self.model = model
        self.year = year
        self.url = url
        self.date_posted = date_posted
        self.size = size
        self.images = images if images is not None else []
        self.price = price
        self.city = city
        self.description = description
        self.region = region
        self.short_description = short_description

    def __repr__(self):
        return (
            f"BikeListing(title={self.title!r}, url={self.url!r}, date_posted={self.date_posted!r}, "
            f"size={self.size!r}, images={self.images!r}, city={self.city}, price={self.price!r}, "
            f"description={self.description!r})"
        )

    def __str__(self):
        return f"{self.title} - {self.price or 'Price not listed'} - {self.date_posted}"

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "brand": self.brand,
            "model": self.model,
            "year": self.year,
            "url": self.url,
            "date_posted": self.date_posted,
            "size": self.size,
            "images": self.images,
            "price": self.price,
            "city": self.city,
            "region": self.region,
            "description": self.description,
            "short_description": self.short_description,
        }


class BikeListing(Base):
    __tablename__ = "bikes"

    id: Mapped[str] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    url: Mapped[str] = mapped_column(nullable=False)
    date_posted: Mapped[str] = mapped_column(nullable=False)
    brand: Mapped[str] = mapped_column(nullable=True)
    model: Mapped[str] = mapped_column(nullable=True)
    year: Mapped[str] = mapped_column(nullable=True)
    size: Mapped[str] = mapped_column(nullable=True)
    price: Mapped[float] = mapped_column(nullable=True)
    city: Mapped[str] = mapped_column(nullable=True)
    region: Mapped[str] = mapped_column(nullable=True)
    description: Mapped[str] = mapped_column(nullable=True)
    short_description: Mapped[str] = mapped_column(nullable=True)
    date_first_seen: Mapped[datetime] = mapped_column(
        DateTime, insert_default=func.now()
    )
    date_last_updated: Mapped[datetime] = mapped_column(
        DateTime, insert_default=func.now()
    )
    images: Mapped[List["BikeImage"]] = relationship(
        back_populates="bike", cascade="all, delete-orphan"
    )


class BikeImage(Base):
    __tablename__ = "bike_images"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    bike_id: Mapped[str] = mapped_column(ForeignKey("bikes.id"), nullable=False)
    image_url: Mapped[str] = mapped_column(nullable=False)

    bike = relationship("BikeListing", back_populates="images")
