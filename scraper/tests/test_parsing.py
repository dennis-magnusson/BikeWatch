from common.models import Size
from scraper.src.parsing import _parse_price, _parse_size, _remove_words

WORDS_TO_REMOVE_ROADBIKE_CATEGORY = [
    "maantiepyörä",
    "road bike",
    "maantie/kisapyörä",
    "Maantie/kisapyörä",
    "aero-maantiepyörä",
    "kisapyörä",
]


def test_remove_words():
    assert (
        _remove_words(
            "Canyon Endurace AL 7.0 Maantiepyörä", WORDS_TO_REMOVE_ROADBIKE_CATEGORY
        )
        == "Canyon Endurace AL 7.0"
    )
    assert (
        _remove_words(
            "Trek Madone SL 6 Gen 8 Road bike", WORDS_TO_REMOVE_ROADBIKE_CATEGORY
        )
        == "Trek Madone SL 6 Gen 8"
    )
    assert (
        _remove_words(
            "BMC Teammachine SLR01 Maantie/kisapyörä", WORDS_TO_REMOVE_ROADBIKE_CATEGORY
        )
        == "BMC Teammachine SLR01"
    )


def test_parse_price():
    assert _parse_price("1 000 €") == 1000
    assert _parse_price("399 €") == 399
    assert _parse_price("€100") == 100
    assert _parse_price("400") == 400
    assert _parse_price("1.950,- €") == 1950
    assert _parse_price("4,990€") == 4990
    assert _parse_price("4 € 990 €") == 4990


def test_parse_sizes():
    assert _parse_size("56cm / M/L") == ((Size.M, Size.L), (56.0, 56.0))
    assert _parse_size("56 M-L") == ((Size.M, Size.L), (56.0, 56.0))
    assert _parse_size("S/47") == ((Size.S, Size.S), (47.0, 47.0))
    assert _parse_size("M/L") == ((Size.M, Size.L), (None, None))
    assert _parse_size("M/L (56/58)") == ((Size.M, Size.L), (56.0, 58.0))

    assert _parse_size("XS") == ((Size.XS, Size.XS), (None, None))
    assert _parse_size("S") == ((Size.S, Size.S), (None, None))
    assert _parse_size("s") == ((Size.S, Size.S), (None, None))
    assert _parse_size("XL") == ((Size.XL, Size.XL), (None, None))
    assert _parse_size("xl") == ((Size.XL, Size.XL), (None, None))

    assert _parse_size("42") == ((None, None), (42.0, 42.0))
    assert _parse_size("46,5") == ((None, None), (46.5, 46.5))
    assert _parse_size("  38  ") == ((None, None), (38.0, 38.0))
    assert _parse_size("58cm") == ((None, None), (58.0, 58.0))
    assert _parse_size("56 cm") == ((None, None), (56.0, 56.0))

    # Additional tests
    assert _parse_size("L/XL") == ((Size.L, Size.XL), (None, None))
    assert _parse_size("M (54/56)") == ((Size.M, Size.M), (54.0, 56.0))
    assert _parse_size("XS-S") == ((Size.XS, Size.S), (None, None))
    assert _parse_size("50-52") == ((None, None), (50.0, 52.0))
