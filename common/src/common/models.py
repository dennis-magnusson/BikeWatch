from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel
from sqlalchemy import DateTime, ForeignKey, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Size(Enum):
    XS = "XS"
    S = "S"
    M = "M"
    L = "L"
    XL = "XL"


class BikeListingBase(BaseModel):
    id: Optional[str] = None
    title: str
    brand: Optional[str] = None
    model: Optional[str] = None
    year: Optional[int] = None
    url: str
    date_posted: Optional[str] = None
    number_size_min: Optional[float] = None
    number_size_max: Optional[float] = None
    letter_size_min: Optional[str] = None
    letter_size_max: Optional[str] = None
    price: Optional[float] = None
    city: Optional[str] = None
    region: Optional[str] = None
    description: Optional[str] = None
    short_description: Optional[str] = None
    images: List[str] = []

    class Config:
        orm_mode = True


class BikeListingData:
    def __init__(
        self,
        id: str,
        title: str,
        brand: str | None,
        model: str | None,
        year: int | None,
        url: str,
        date_posted: str | None,
        number_size_min: float | None,
        number_size_max: float | None,
        letter_size_min: Size | None,
        letter_size_max: Size | None,
        images: List[str] | None,
        price: float | None,
        city: str | None,
        region: str | None,
        description: str | None,
        short_description: str | None,
        category: str | None = None,
    ):
        self.id = id
        self.title = title
        self.brand = brand
        self.model = model
        self.year = year
        self.url = url
        self.date_posted = date_posted
        self.number_size_min = number_size_min
        self.number_size_max = number_size_max
        self.letter_size_min = letter_size_min
        self.letter_size_max = letter_size_max
        self.images = images if images is not None else []
        self.price = price
        self.city = city
        self.description = description
        self.region = region
        self.short_description = short_description
        self.category = category

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "brand": self.brand,
            "model": self.model,
            "year": self.year,
            "url": self.url,
            "date_posted": self.date_posted,
            "number_size_max": self.number_size_max,
            "number_size_min": self.number_size_min,
            "letter_size_max": self.letter_size_max,
            "letter_size_min": self.letter_size_min,
            "images": self.images,
            "price": self.price,
            "city": self.city,
            "region": self.region,
            "description": self.description,
            "short_description": self.short_description,
            "category": self.category,
        }


class Base(DeclarativeBase):
    pass


class BikeListing(Base):
    __tablename__ = "bike"

    id: Mapped[str] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    url: Mapped[str] = mapped_column(nullable=False)
    date_posted: Mapped[str] = mapped_column(nullable=False)
    brand: Mapped[str] = mapped_column(nullable=True)
    model: Mapped[str] = mapped_column(nullable=True)
    year: Mapped[str] = mapped_column(nullable=True)
    letter_size_min: Mapped[str] = mapped_column(nullable=True)
    letter_size_max: Mapped[str] = mapped_column(nullable=True)
    number_size_min: Mapped[float] = mapped_column(nullable=True)
    number_size_max: Mapped[float] = mapped_column(nullable=True)
    price: Mapped[float] = mapped_column(nullable=True)
    city: Mapped[str] = mapped_column(nullable=True)
    region: Mapped[str] = mapped_column(nullable=True)
    description: Mapped[str] = mapped_column(nullable=True)
    short_description: Mapped[str] = mapped_column(nullable=True)
    category: Mapped[str] = mapped_column()
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
    __tablename__ = "bike_image"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    bike_id: Mapped[str] = mapped_column(ForeignKey("bike.id"), nullable=False)
    image_url: Mapped[str] = mapped_column(nullable=False)

    bike = relationship("BikeListing", back_populates="images")
