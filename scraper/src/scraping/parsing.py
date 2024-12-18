import re

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
            size = val
        elif keyword_match(keywords["model"], key):
            model = val
        elif keyword_match(keywords["brand"], key):
            brand = val
        elif keyword_match(keywords["city"], key):
            city = val
        elif keyword_match(keywords["year"], key):
            year = val
        elif keyword_match(keywords["price"], key):
            price = val
        elif keyword_match(keywords["description"], key):
            description = val
        elif keyword_match(keywords["short_description"], key):
            short_description = val
        elif keyword_match(keywords["region"], val):
            region = val

    return brand, model, price, year, size, region, city, description, short_description


def parse_raw_title(soup):
    post_title = soup.find("h1").find_all("span")[-1].text.rsplit(",", maxsplit=2)
    title = post_title[0]
    return title


def parse_date_posted(soup):
    return soup.find("time")["datetime"]


def parse_raw_images(soup):
    image_links = soup.find("article").find_all(
        "a", href=re.compile(r"cdn2\.fillaritori\.com")
    )
    image_links = [link["href"] for link in image_links]
    image_links = [f"https:{link}" for link in image_links if link.startswith("//")]
    return image_links
