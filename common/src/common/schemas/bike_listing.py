from enum import Enum
from typing import List, Optional, Tuple

from pydantic import BaseModel


class Size(Enum):
    XS = (47, 51)
    S = (52, 54)
    M = (55, 57)
    L = (58, 60)
    XL = (61, 64)

    @property
    def size_range(self) -> Tuple[int, int]:
        return self.value

    @property
    def min_size(self) -> int:
        return self.value[0]

    @property
    def max_size(self) -> int:
        return self.value[1]

    def __str__(self):
        return self.name


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
    images: List[str] = []
    category: Optional[str] = None

    def matches_size(self, size: float, flexibility: bool = False) -> bool:
        """
        Check if the given numerical size matches this bike listing.
        Args:
            size: The frame size in centimeters to check
            flexibility: If True, allow ±1cm flexibility in size matching
        Returns:
            bool: True if the size matches, False otherwise
        """

        min_size = size - 1 if flexibility else size
        max_size = size + 1 if flexibility else size

        if all((self.number_size_min, self.number_size_max)):
            return self.number_size_min <= max_size and self.number_size_max >= min_size

        if all((self.letter_size_min, self.letter_size_max)):
            try:
                min_number = Size[self.letter_size_min].min_size
                max_number = Size[self.letter_size_max].max_size
                return min_number <= max_size and max_number >= min_size
            except KeyError:  # Size not found
                return False

        return False

    def matches_price_range(self, min_price: float, max_price: float) -> bool:
        """
        Check if the price of this bike listing is within the given price range.
        Args:
            min_price: The minimum price to check
            max_price: The maximum price to check
        Returns:
            bool: True if the price is within the range, False otherwise
        """
        return bool(self.price) and min_price <= self.price <= max_price

    class Config:
        from_attributes = True
        json_encoders = {Size: lambda v: v.name if v else None}
