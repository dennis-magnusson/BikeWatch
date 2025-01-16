import re
from typing import List, Optional, Tuple

from common.models import Size

keywords = {
    "size": ["koko", "rungon koko", "size", "frame size"],
    "model": ["malli", "model"],
    "brand": ["merkki", "brand"],
    "year": ["vuosimalli", "vm.", "vuosi"],
    "region": ["maakunta", "province"],
    "city": ["paikkakunta", "kaupunki", "city"],
    "price": ["hinta", "price"],
    "short_description": ["lyhyt kuvaus"],
    "description": ["kuvaus"],
}

words_to_remove_from_titles = {
    "road": [
        "maantiepyörä",
        "road bike",
        "maantie/kisapyörä",
        "Maantie/kisapyörä",
        "aero-maantiepyörä",
        "kisapyörä",
    ],
    "gravel": ["gravel"],
    "triathlon": [],
    "hybrid": [],
    "mountain_rigid": [],
    "mountain_hardtail": [],
    "electric_flat": [],
    "electric_mountain": [],
    "fatbike": [],
}


def keyword_match(keywords, string):
    return any(kw in string.lower() for kw in keywords)


def parse_raw_description(soup):
    ps = [p.text for p in soup.find("article").find_all("p")]

    model = None
    brand = None
    city = None
    region = None
    year = None
    price = None
    short_description = None
    description = None

    # TODO: Make sure that multiple matches don't overwrite themselves. What if there are more than one match and the "correct" match is overwritten with the latter false match?

    for p in ps:
        clean_text = p.replace("\xa0", " ").strip()

        if clean_text.strip() == "":
            continue
        splitted = clean_text.split(":", maxsplit=1)

        if len(splitted) == 1:
            continue

        key = splitted[0]
        try:
            val = splitted[1].strip()
        except IndexError:
            raise IndexError(f"IndexError: {splitted}, p: {p}")

        if keyword_match(keywords["size"], key):
            letter_size, numerical_size = parse_size(val)

        elif keyword_match(keywords["model"], key):
            model = val
        elif keyword_match(keywords["brand"], key):
            brand = val
        elif keyword_match(keywords["city"], key):
            city = val
        elif keyword_match(keywords["year"], key):
            year = val
        elif keyword_match(keywords["price"], key):
            price = parse_price(val)
        elif keyword_match(keywords["description"], key):
            description = val
        elif keyword_match(keywords["short_description"], key):
            short_description = val
        elif keyword_match(keywords["region"], key):
            region = val

    return (
        brand,
        model,
        price,
        year,
        numerical_size[0],
        numerical_size[1],
        letter_size[0],
        letter_size[1],
        region,
        city,
        description,
        short_description,
    )


def parse_raw_title(soup, category: str) -> str:
    post_title = soup.find("h1").find_all("span")[-1].text.rsplit(",", maxsplit=2)
    title = remove_words(post_title[0], words_to_remove_from_titles.get(category, []))
    return title


def remove_words(string: str, remove_words: List[str]) -> str:
    words_to_remove = remove_words + [word.capitalize() for word in remove_words]
    for word in words_to_remove:
        string = string.replace(f" {word}", "")
    return string


def parse_price(price_str):
    """
    Parses a price string and returns the integer value.
    - Removes non-numeric characters except commas and periods.
    - Replaces commas with periods if they are used as decimal separators.
    - Checks if the last separator is a decimal point with exactly two digits after it.
    - Treats all separators as thousand separators if the above condition is not met.
    - Returns None if the conversion fails.
    """
    clean_str = re.sub(r"[^\d,\.]", "", price_str)
    if "," in clean_str and "." not in clean_str:
        clean_str = clean_str.replace(",", ".")
    if "." in clean_str:
        parts = clean_str.split(".")
        if len(parts[-1]) == 2:
            clean_str = clean_str.replace(",", "")
        else:
            clean_str = clean_str.replace(".", "").replace(",", "")
    else:
        clean_str = clean_str.replace(",", "")
    try:
        return int(float(clean_str))
    except ValueError:
        return None


def parse_date_posted(soup):
    return soup.find("time")["datetime"]


def parse_raw_images(soup):
    image_links = soup.find("article").find_all(
        "a", href=re.compile(r"cdn2\.fillaritori\.com")
    )
    image_links = [link["href"] for link in image_links]
    image_links = [f"https:{link}" for link in image_links if link.startswith("//")]
    return image_links


def parse_size(
    size_str: str,
) -> Tuple[
    Tuple[Optional[Size], Optional[Size]], Tuple[Optional[float], Optional[float]]
]:
    """
    Parses a size string and returns the corresponding size values.
    - Returns the ranges for number sizes if present (None otherwise).
    - Returns the ranges (min and max) for letter sizes if present (None otherwise).
    - If the size is not a range the same value is returned for both min and max.
    """
    # replace all , with .
    size_str = size_str.replace(",", ".")
    size_str = size_str.replace("cm", "")
    size_str = size_str.replace(" ", "")

    possible_letter_size_substrings = {e.value: e for e in Size}

    numerical_range_match = re.search(r"(\d+\.?\d*)[\s/-]+(\d+\.?\d*)", size_str)
    if not numerical_range_match:
        single_numerical_match = re.search(r"(\d+\.?\d*)", size_str)

    letter_range_match = re.search(
        r"(XS|S|M|L|XL)[\s/-]+(XS|S|M|L|XL)", size_str, re.IGNORECASE
    )
    single_letter_match = re.search(r"(XS|S|M|L|XL)", size_str, re.IGNORECASE)

    numerical_result = (None, None)
    letter_result = (None, None)

    if numerical_range_match:
        numerical_result = (
            float(numerical_range_match.group(1)),
            float(numerical_range_match.group(2)),
        )
    elif single_numerical_match:
        numerical_result = (
            float(single_numerical_match.group(1)),
            float(single_numerical_match.group(1)),
        )

    if letter_range_match:
        letter_result = (
            possible_letter_size_substrings[letter_range_match.group(1).upper()],
            possible_letter_size_substrings[letter_range_match.group(2).upper()],
        )
    elif single_letter_match:
        letter_result = (
            possible_letter_size_substrings[single_letter_match.group(1).upper()],
            possible_letter_size_substrings[single_letter_match.group(1).upper()],
        )

    return (letter_result, numerical_result)
