from enum import Enum
from typing import List, Optional

from pydantic import BaseModel


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
    category: Optional[str] = None

    class Config:
        orm_mode = True
