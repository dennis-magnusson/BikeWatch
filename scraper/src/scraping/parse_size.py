import logging
import re
from enum import Enum


class Size(Enum):
    XS = "XS"
    S = "S"
    M = "M"
    L = "L"
    XL = "XL"


def parse_size(size_str):
    size_str = size_str.upper().strip()
    size_mapping = {
        "XS": Size.XS,
        "S": Size.S,
        "M": Size.M,
        "L": Size.L,
        "XL": Size.XL,
    }
    if size_str in size_mapping:
        return size_mapping[size_str]
    numeric_str = re.sub(r"[^\d]", "", size_str)  # Remove non-numeric characters
    try:
        return float(numeric_str)
    except ValueError:
        logging.error(f"Could not parse size: {size_str=}")