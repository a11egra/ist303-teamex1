
import pytest
from problem6_code import parse_time_expression


def test_type_guard_non_string_raises():
    with pytest.raises(Exception):
        parse_time_expression(123)  


# --- Example calls from the brief (must match exactly) -----------------------

@pytest.mark.parametrize("text, expected", [
    ("3:30pm", (15, 30)),
    ("quarter to midnight", (23, 45)),
    ("half past 7", (7, 30)),
    ("14:45", (14, 45)),
    ("noon", (12, 0)),
    ("12 PM", (12, 0)),
    ("12 AM", (0, 0)),
])
def test_examples_match_spec(text, expected):
    out = parse_time_expression(text)
    assert out == expected, f"test failed: expected {expected} for {text!r}, got {out!r}"


# --- Additional format coverage  -------------------------

@pytest.mark.parametrize("text, expected", [
    ("3:30", (3, 30)),          # standard time
    ("03:30", (3, 30)),         # leading zero
    ("3pm", (15, 0)),           # hour with AM/PM
    ("2 AM", (2, 0)),
    ("midnight", (0, 0)),       # special word
    ("quarter past three", (3, 15)),
    ("quarter to 5", (4, 45)),
])
def test_supported_formats(text, expected):
    out = parse_time_expression(text)
    assert out == expected, f"test failed: expected {expected} for {text!r}, got {out!r}"


# --- Edge cases & normalization ----------------------------------------------

@pytest.mark.parametrize("text, expected", [
    ("  3:30PM  ", (15, 30)),   # whitespace
    ("12 pm", (12, 0)),         # noon edge case in 12-hour
    ("12 am", (0, 0)),          # midnight edge case in 12-hour
    ("3:03", (3, 3)),           # leading zero minute normalized to int
])
def test_edge_cases(text, expected):
    out = parse_time_expression(text)
    assert out == expected, f"test failed: expected {expected} for {text!r}, got {out!r}"


# --- Unparseable inputs should return None -----------------------------------

@pytest.mark.parametrize("text", [
    "",               # empty after strip
    "25:00",          # invalid hour
    "13:75",          # invalid minute
    "tomorrow",       # unsupported phrase
])
def test_returns_none_when_unparseable(text):
    out = parse_time_expression(text)
    assert out is None, f"test failed: expected None for {text!r}, got {out!r}"


# --- Contract: return type is either tuple(int,int) or None ------------------

@pytest.mark.parametrize("text", [
    "3:30pm",
    "quarter to midnight",
    "half past 7",
    "14:45",
    "noon",
    "12 PM",
    "12 AM",
])
def test_return_type_contract(text):
    out = parse_time_expression(text)
    assert (out is None) or (isinstance(out, tuple) and len(out) == 2 and all(isinstance(x, int) for x in out)),         f"test failed: return type must be tuple(int,int) or None for {text!r}, got {type(out)} {out!r}"


# --- Additional requirement: bounds of returned time -------------------------

@pytest.mark.parametrize("text", [
    "3:30pm",
    "quarter to midnight",
    "half past 7",
    "14:45",
    "noon",
    "12 PM",
    "12 AM",
    "03:30",
    "3pm",
    "2 AM",
])
def test_bounds_of_returned_time(text):
    out = parse_time_expression(text)
    assert out is not None, f"test failed: expected a parsed time for {text!r}, got None"
    h, m = out
    assert 0 <= h <= 23 and 0 <= m <= 59, f"test failed: hour/minute out of range for {text!r}: {(h, m)}"
