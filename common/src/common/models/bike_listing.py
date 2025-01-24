from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from common.models.base import Base
from common.models.bike_image import BikeImage


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
    images: Mapped[list["BikeImage"]] = relationship(
        back_populates="bike", cascade="all, delete-orphan"
    )
