from scraper.src.scraping.parsing import Size, parse_price, parse_size


def test_parse_price():
    assert parse_price("1 000 €") == 1000
    assert parse_price("399 €") == 399
    assert parse_price("€100") == 100
    assert parse_price("400") == 400
    assert parse_price("1.950,- €") == 1950
    assert parse_price("4,990€") == 4990
    assert parse_price("4 € 990 €") == 4990


def test_parse_sizes():
    assert parse_size("XS") == Size.XS
    assert parse_size("S") == Size.S
    assert parse_size("M") == Size.M
    assert parse_size("L") == Size.L
    assert parse_size("XL") == Size.XL
    assert parse_size("42") == 42
    assert parse_size("  38  ") == 38
    assert parse_size("xl") == Size.XL
    assert parse_size("s") == Size.S
    assert parse_size("58cm") == 58
    assert parse_size("56 cm") == 56
    assert parse_size("56cm / M") == 56
    assert parse_size("S/47") == 47
    try:
        parse_size("unknown")
    except ValueError as e:
        assert str(e) == "Could not parse size: size_str='UNKNOWN'"