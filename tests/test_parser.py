import seql
import pytest

test_cases = [
    (
        "SELECT IPP WITH 3 EVENT FROM biologie AFTER 5 DAY WHERE code = 'ATC'",
        {
            "fields": ["IPP"],
            "events": [
                {
                    "count": 3,
                    "domain": "biologie",
                    "direction": "AFTER",
                    "interval": 5,
                    "unite": "DAY",
                    "start_date": None,
                    "end_date": None,
                    "where": {"field": "code", "operator": "=", "value": "ATC"},
                }
            ],
        },
    ),
    (
        "SELECT IPP WITH 3 EVENT FROM biologie  WHERE code = 'ATC'",
        {
            "fields": ["IPP"],
            "events": [
                {
                    "count": 3,
                    "domain": "biologie",
                    "direction": None,
                    "interval": None,
                    "unite": None,
                    "start_date": None,
                    "end_date": None,
                    "where": {"field": "code", "operator": "=", "value": "ATC"},
                }
            ],
        },
    ),
    (
        "SELECT IPP WITH 3 EVENT FROM biologie AFTER 5 DAY  WHERE code = 'ATC'",
        {
            "fields": ["IPP"],
            "events": [
                {
                    "count": 3,
                    "domain": "biologie",
                    "direction": "AFTER",
                    "interval": 5,
                    "unite": "DAY",
                    "start_date": None,
                    "end_date": None,
                    "where": {"field": "code", "operator": "=", "value": "ATC"},
                }
            ],
        },
    ),
]


@pytest.mark.parametrize("query,expected_obj", test_cases, ids=range(len(test_cases)))
def test_query(query: str, expected_obj):

    observed_obj = seql.parse(query)

    assert observed_obj == expected_obj
