from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from common.models.base import Base


class BikeImage(Base):
    __tablename__ = "bike_image"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    bike_id: Mapped[str] = mapped_column(ForeignKey("bike.id"), nullable=False)
    image_url: Mapped[str] = mapped_column(nullable=False)

    bike = relationship("BikeListing", back_populates="images")
