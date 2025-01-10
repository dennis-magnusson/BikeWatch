import logging
import re
from typing import Optional, Tuple

from common.models import Size


def parse_size(
    size_str: str,
) -> Tuple[Optional[Size], Optional[Size], Optional[float], Optional[float]]:
    """
    Parses a size string and returns the corresponding size values.
    - Returns the ranges for number sizes if present (None otherwise).
    - Returns the ranges (min and max) for letter sizes if present (None otherwise).
    - If the size is not a range the same value is returned for both min and max.
    """
    raise NotImplementedError("Not implemented yet")
    return ("M", "L", 50.0, 52.0)
