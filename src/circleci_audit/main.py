import argparse
import logging
import sys

from circleci_audit import cli
from circleci_audit.known_error import KnownError


def main():
    logging.basicConfig(level=logging.INFO)

    parser = argparse.ArgumentParser()
    sub_parsers = parser.add_subparsers(dest="command", required=True)

    projects_parser = sub_parsers.add_parser("validate")
    projects_parser.set_defaults(func=lambda _: cli.validate_configuration())

    projects_parser = sub_parsers.add_parser("repos")
    projects_parser.set_defaults(func=lambda _: cli.list_repositories())

    args = parser.parse_args()

    try:
        args.func(args)
    except KnownError as ex:
        print(ex.args[0], file=sys.stderr)
        exit(1)


if __name__ == "__main__":
    main()
