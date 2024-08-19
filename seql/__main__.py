import argparse
import sys
import seql


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="SEQL transpiler")

    subparsers = parser.add_subparsers(dest="command")
    subparsers.required = True

    # Transpiler
    transpile_parser = subparsers.add_parser("transpile", help="Transpile SEQL to any engines")
    transpile_parser.add_argument(
        "--engine",
        "-e",
        required=False,
        default="json",
        help="engine target",
        choices=seql.transpiler._get_engines(),
    )
    transpile_parser.add_argument("query", help="SEQL query to transpile")

    # Schema
    schema_parser = subparsers.add_parser("schema", help="Display engine schema")
    schema_parser.add_argument(
        "--engine",
        "-e",
        required=False,
        default="json",
        help="engine target",
        choices=seql.transpiler._get_engines(),
    )
    schema_parser.add_argument(
        "--fields", nargs="+", default=["SAMPLE_ID"], help="Custom fields", required=False
    )
    schema_parser.add_argument(
        "--table_name", default="events", help="Custom table name", required=False
    )

    args = parser.parse_args()

    if args.command == "transpile":

        try:
            result = seql.transpile(args.query, engine=args.engine)
            print(result)
        except Exception as e:
            print(e)

    if args.command == "schema":

        try:
            result = seql.schema(fields=args.fields, table_name=args.table_name, engine=args.engine)
            print(result)
        except Exception as e:
            print(f"Cannot create schema for engine {engine}")
