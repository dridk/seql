import pytest
import seql

ENGINES = ["duckdb"]


@pytest.mark.parametrize("engine", ENGINES)
def test_schema(engine):
    schema = seql.schema(["IPP"], engine=engine)
    assert isinstance(schema, str)


@pytest.mark.parametrize("engine", ENGINES)
def test_transpile(engine):
    query = "SELECT IPP WITH 3 EVENT FROM biologie AFTER 5 DAY  WHERE code = 'ATC'"
    transpiled = seql.transpile(query, engine=engine)
    assert isinstance(transpiled, str)
