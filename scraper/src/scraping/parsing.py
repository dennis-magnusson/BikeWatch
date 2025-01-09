import re
from enum import Enum

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


def keyword_match(keywords, string):
    return any(kw in string.lower() for kw in keywords)


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
        return int(numeric_str)
    except ValueError:
        raise ValueError(f"Could not parse size: {size_str=}")


def parse_raw_description(soup):
    ps = [p.text for p in soup.find("article").find_all("p")]

    size = None
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
            size = parse_size(val)
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

    return brand, model, price, year, size, region, city, description, short_description


def parse_raw_title(soup):
    post_title = soup.find("h1").find_all("span")[-1].text.rsplit(",", maxsplit=2)
    title = post_title[0]
    return title


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
