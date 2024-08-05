import os
from .engines import duckdb, sqlite


def create_schema(fields: list[str]) -> str:
    pass


def transpile(query: str, engine="duckdb") -> str:
    pass
