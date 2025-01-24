from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from common.models.base import Base


class UserAlert(Base):
    __tablename__ = "user_alert"

    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)
    min_price = Column(Float)
    max_price = Column(Float)
    category = Column(String)
    city = Column(String)
    region = Column(String)
    size = Column(Float)
    size_flexibility = Column(Boolean)

    alerted_listings = relationship("AlertedListing", back_populates="user_alert")


class AlertedListing(Base):
    __tablename__ = "alerted_listing"

    id = Column(Integer, primary_key=True, index=True)
    alert_id = Column(Integer, ForeignKey("user_alert.id"))
    listing_id = Column(Integer, ForeignKey("bike.id"))
    user_alert = relationship("UserAlert", back_populates="alerted_listings")
