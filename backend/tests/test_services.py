from datetime import datetime
from pathlib import Path

import services


def test_parse_date_removes_ordinal_suffix_and_comma():
    assert services.parse_date("12th May, 2026") == datetime(2026, 5, 12)


def test_parse_date_accepts_abbreviated_month():
    assert services.parse_date("1st Jun 2026") == datetime(2026, 6, 1)


def test_get_series_letter_handles_common_labels():
    assert services.get_series_letter("EQAR Series F") == "F"
    assert services.get_series_letter("eqar f") == "F"


def test_is_car_series_is_word_aware():
    assert services.is_car_series("CAR Series E")
    assert not services.is_car_series("EQAR Series E")


def test_extract_all_valuations_from_saved_pdf_text_fixture():
    fixture = Path(__file__).parent / "fixtures" / "valuation_report.txt"
    valuations = services._extract_valuations_from_text(fixture.read_text())
    assert valuations == [
        (datetime(2026, 5, 12), 101.25),
        (datetime(2026, 6, 1), 99.50),
    ]


def test_find_series_link_uses_fuzzy_matching_for_separator_variations():
    links = [{"fn_upper": "CAR SERIES E REPORT", "filename": "CAR_SERIES_E_REPORT"}]
    assert services.find_series_link(links, "CAR E") == links[0]
