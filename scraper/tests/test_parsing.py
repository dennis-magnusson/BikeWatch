from scraper.src.scraping.parsing import parse_price


def test_parse_price():
    assert parse_price("1 000 €") == 1000
    assert parse_price("399 €") == 399
    assert parse_price("€100") == 100
    assert parse_price("400") == 400
    assert parse_price("1.950,- €") == 1950
    assert parse_price("4,990€") == 4990
    assert parse_price("4 € 990 €") == 4990