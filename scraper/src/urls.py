from dataclasses import dataclass


@dataclass
class Category:
    url_id: str
    name: str


def get_url(category: Category) -> str:
    return (
        "https://www.fillaritori.com/forum/"
        + category.url_id
        + "/page/{}/?filterByState=8"
    )


categories = [
    Category(
        url_id="54-maantie",
        name="road",
    ),
    Category(
        url_id="55-cyclocrossgravel",
        name="gravel",
    ),
    Category(
        url_id="56-hybridfitness",
        name="hybrid",
    ),
    # Category(
    #     url_id="57-joustamattomat",
    #     name="mountain_rigid",
    # ),
    # Category(
    #     url_id="58-etujousitetut",
    #     name="mountain_hardtail",
    # ),
    # Category(
    #     url_id="69-triathlonaika-ajo",
    #     name="triathlon",
    # ),
    # Category(
    #     url_id="70-fatbiket",
    #     name="fatbike",
    # ),
    # Category(
    #     url_id="84-tasamaa",
    #     name="electric_flat",
    # ),
    # Category(
    #     url_id="85-maasto",
    #     name="electric_mountain",
    # ),
]
