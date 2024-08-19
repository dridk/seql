import seql
from textwrap import dedent
from typing import Any

OPERATORS = {"$and": "AND", "$or": "OR"}


def schema(fields: list[str] = ["ID"], table_name: str = "events") -> str:

    fields = ",".join([f"{i} VARCHAR" for i in fields])
    sql = f"""
    CREATE table {table_name}(
        {fields},
        TS TIMESTAMP,
        DOMAIN VARCHAR,
        CODE VARCHAR,
        VALUE VARCHAR,        
    )

    """
    return sql


def from_obj(obj: dict, table_name: str = "events") -> str:
    """
    Convert object returned by seql.parse() to SQL select query

    Args:
        obj (dict): a nested dictionnary returned by seql.parse
        table_name (str): Event table name. Default value = 'events'

    """

    def quoting(value: Any) -> str:
        """
        Transform any value to an SQL value.
        For instance, add 'quote' for string value
        """
        if type(value) == str:
            return f"'{value}'"

        return str(value)

    def create_where(where: obj) -> str:
        """
        Recursive function to generate SQL where clause from the `where` object
        """
        if len(where.keys()) == 3:
            field, operator, value = where["field"], where["operator"], where["value"]
            value = quoting(value)
            return f"{field} {operator} {value}"

        if len(where.keys()) == 1:
            operator = list(where.keys())[0]
            sql_operator = OPERATORS.get(operator, "AND")

            query = f" {sql_operator} ".join([create_where(clause) for clause in where[operator]])
            return f"({query})"

    # Loop over all events and generate SQL query

    fields = ",".join(obj["fields"])
    events = obj["events"]
    event_queries = []
    for index, event in enumerate(events):
        where_clause = create_where(event["where"])
        query = f"""event{index} AS (SELECT * FROM {table_name} WHERE domain ='{event['domain']}' AND {where_clause})""".format(
            **event
        )

        event_queries.append((query))

    query = ["WITH"] + event_queries
    query = "\n".join(query)

    query += "\nSELECT * FROM event0"
    if len(events) > 1:
        for index, event in enumerate(events[1:]):
            index += 1
            query += f"\nINNER JOIN event{index} ON "
            conditions = []
            for field in obj["fields"]:
                conditions.append(f"event{index}.{field} = event0.{field}")

            op = "<" if event["direction"] == "BEFORE" else ">"
            conditions.append(
                f"event{index}.ts {op} event0.ts + INTERVAL {event['interval']} {event['unite']}"
            )

            query += " AND ".join(conditions)

    print("ICI", query)
    return query


def transpile(query: str) -> str:

    return from_obj(seql.parse(query))
