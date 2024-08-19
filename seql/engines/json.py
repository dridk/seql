import seql
import json


def schema(fields: list[str] = ["ID"], table_name: str = "events") -> str:

    json_form = {
        "fields": [
            {
                "name": "fields",
                "type": "array",
                "description": "Fields lists",
                "items": {"type": "string", "description": "Un champ dans la liste des champs"},
            }
        ],
        "events": [
            {
                "count": {"type": "integer", "description": "Event count", "default": 1},
                "domain": {
                    "type": "string",
                    "description": "Event domain",
                },
                "direction": {
                    "type": "string",
                    "description": "time relationship with previous event",
                    "enum": ["AFTER", "BEFORE"],
                },
                "start_date": {
                    "type": "string",
                    "format": "date",
                    "description": "start date of event",
                },
                "end_date": {
                    "type": "string",
                    "format": "date",
                    "description": "End date of event",
                },
                "interval": {
                    "type": "integer",
                    "description": "Interval of event. For instance '5 DAY' or '10 MONTH'",
                },
                "unite": {
                    "type": "string",
                    "description": "Unit of event. ",
                    "enum": ["SECOND", "MINUTE", "HOUR", "DAY", "MONTH", "YEAR"],
                },
                "where": {
                    "type": "string",
                    "description": "Recursive condition filter",
                },
                "required": ["field", "operator", "value"],
            },
        ],
    }

    return json.dumps(json_form, indent=4)


def transpile(query: str) -> str:

    return json.dumps(seql.parse(query), indent=4)
