from scraper.src.scraping import get_category_page_count


def test_get_category_page_count():
    assert (
        get_category_page_count(
            "https://www.fillaritori.com/forum/55-cyclocrossgravel/page/{}/?filterByState=8"
        )
        == 23
    )  # NOTE: This test will fail if the number of pages changes
