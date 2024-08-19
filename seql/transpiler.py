import json
import os
import pkgutil
import importlib
from typing import Callable
from .engines import duckdb, sqlite
from .parser import parse


class TranspilerError(Exception):
    pass


def _get_engines() -> list[str]:
    """
    Return engines name available as module from engines packages
    """
    package = importlib.import_module("seql.engines")
    package_path = package.__path__

    modules = [name for _, name, is_pkg in pkgutil.iter_modules(package_path) if not is_pkg]
    return modules


def _get_engine_fct(engine: str, fct_name: str) -> Callable:
    """
    Return module function from the name
    """
    module = importlib.import_module(f"seql.engines.{engine}")
    fct = getattr(module, fct_name)
    return fct


def schema(fields: list[str], table_name: str = "events", *, engine: str = "json") -> str:
    """
    Return table schema for the specific engine
    """

    if engine not in _get_engines():
        raise TranspilerError(f"engine {engine} does not exists")

    schema_fct = _get_engine_fct(engine, "schema")
    if not callable(schema):
        raise TranspilerError(f"Cannot create schema function from engine {engine}")

    return schema_fct(fields, table_name)


def transpile(query: str, *, engine: str = "json") -> str:
    """
    Create engine Query from a SEQL Query

    """

    if engine not in _get_engines():
        raise TranspilerError(f"engine {engine} does not exists")

    transpile_fct = _get_engine_fct(engine, "transpile")

    if not callable(transpile):
        raise TranspilerError(f"Cannot create transpile function from engine {engine}")

    return transpile_fct(query)
