import os
from textx import metamodel_from_file
import json
import textx


GRAMMAR_PATH = os.path.dirname(os.path.abspath(__file__)) + "/grammar.tx"
MAP_OPERATOR = {"AND": "$and", "OR": "$or"}


def _parse_where_expression(expression) -> dict:

    if expression is None:
        return None

    if len(expression.op) == 3:
        operator = MAP_OPERATOR.get(expression.op[1], "$and")

        operands = [expression.op[0].op, expression.op[2].op]
        conditions = []
        for operand in operands:
            if operand.__class__.__name__ == "WhereTerm":
                condition = {"field": operand.field, "operator": operand.op, "value": operand.val}
            if operand.__class__.__name__ == "WhereExpression":
                condition = _parse_where_expression(operand)
            conditions.append(condition)

        return {operator: conditions}

    if len(expression.op) == 1:
        operand = expression.op[0].op
        condition = {"field": operand.field, "operator": operand.op, "value": operand.val}
        return condition


def parse(query: str) -> dict:
    """
    From a SEQL query, generate a python object
    """
    metamodel = metamodel_from_file(GRAMMAR_PATH)
    metamodel.register_obj_processors({"Tuple": lambda x: x.items})
    model = metamodel.model_from_str(query)

    results = {}

    results["fields"] = model.fields
    events = []
    for event in model.events:

        # Parse where clause
        where = _parse_where_expression(event.condition)

        events.append(
            {
                "count": event.count,
                "domain": event.domain,
                "direction": event.direction,
                "start_date": event.start_date,
                "end_date": event.end_date,
                "interval": None if event.interval is None else event.interval.number,
                "unite": None if event.interval is None else event.interval.unite,
                "where": where,
            }
        )
        results["events"] = events
    return results


query = """

SELECT sacha WITH 
3 EVENT FROM biologie AFTER 3 DAY BETWEEN 02/03/2010 AND 04/04/2020 WHERE code = 'ferritine' AND (value > 40 OR value < 100)
ANY EVENT FROM pmsi AFTER 3 DAY WHERE code IN ('Z50','252')
ANY EVENT FROM drugs AFTER 5 DAY WHERE code = 'ATC54'
    
"""
