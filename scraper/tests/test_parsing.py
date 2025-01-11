import sys

print("Modules found in the file:")
for module in sorted(sys.modules.keys()):
    print(module)

from common.models import Size
from scraper.src.scraping.parsing import parse_price, parse_size


def test_parse_price():
    assert parse_price("1 000 €") == 1000
    assert parse_price("399 €") == 399
    assert parse_price("€100") == 100
    assert parse_price("400") == 400
    assert parse_price("1.950,- €") == 1950
    assert parse_price("4,990€") == 4990
    assert parse_price("4 € 990 €") == 4990


def test_parse_sizes():
    assert parse_size("56cm / M/L") == ((Size.M, Size.L), (56.0, 56.0))
    assert parse_size("56 M-L") == ((Size.M, Size.L), (56.0, 56.0))
    assert parse_size("S/47") == ((Size.S, Size.S), (47.0, 47.0))
    assert parse_size("M/L") == ((Size.M, Size.L), (None, None))
    assert parse_size("M/L (56/58)") == ((Size.M, Size.L), (56.0, 58.0))

    assert parse_size("XS") == ((Size.XS, Size.XS), (None, None))
    assert parse_size("S") == ((Size.S, Size.S), (None, None))
    assert parse_size("s") == ((Size.S, Size.S), (None, None))
    assert parse_size("XL") == ((Size.XL, Size.XL), (None, None))
    assert parse_size("xl") == ((Size.XL, Size.XL), (None, None))

    assert parse_size("42") == ((None, None), (42.0, 42.0))
    assert parse_size("46,5") == ((None, None), (46.5, 46.5))
    assert parse_size("  38  ") == ((None, None), (38.0, 38.0))
    assert parse_size("58cm") == ((None, None), (58.0, 58.0))
    assert parse_size("56 cm") == ((None, None), (56.0, 56.0))

    # Additional tests
    assert parse_size("L/XL") == ((Size.L, Size.XL), (None, None))
    assert parse_size("M (54/56)") == ((Size.M, Size.M), (54.0, 56.0))
    assert parse_size("XS-S") == ((Size.XS, Size.S), (None, None))
    assert parse_size("50-52") == ((None, None), (50.0, 52.0))
