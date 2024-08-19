import seql
import duckdb


def test_schema():

    conn = duckdb.connect(":memory:")
    schema = seql.duckdb.schema()
    conn.sql(schema)


def test_transpile():

    query = """
    SELECT ID WITH
    ANY EVENT FROM biologie WHERE code = 'ferritine'  AND ( value > 10 OR value < 100)
    3 EVENT FROM pmsi AFTER 3 DAY WHERE code = 'ATC'
    """

    observed = seql.duckdb.transpile(query)

    expected = """WITH
event0 AS (SELECT * FROM events WHERE domain ='biologie' AND (code = 'ferritine' AND (value > 10 OR value < 100)))
event1 AS (SELECT * FROM events WHERE domain ='pmsi' AND code = 'ATC')
SELECT * FROM event0
INNER JOIN event1 ON event1.ID = event0.ID AND event1.ts > event0.ts + INTERVAL 3 DAY

"""

    expected = expected.strip()
    print("EXPECTED")
    print(expected)
    print("OBSERVED")
    print(observed)
    assert observed == expected
