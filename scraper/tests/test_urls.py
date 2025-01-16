from scraper.src.scraping.urls import categories, get_url


def test_get_url():
    assert (
        get_url(categories[0])
        == "https://www.fillaritori.com/forum/54-maantie/page/{}/?filterByState=8"
    )
