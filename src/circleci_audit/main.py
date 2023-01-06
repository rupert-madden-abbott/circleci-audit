import argparse
import logging
import sys

from circleci_audit import cli
from circleci_audit.known_error import KnownError


def main():
    logging.basicConfig(level=logging.INFO)

    parser = argparse.ArgumentParser()
    sub_parsers = parser.add_subparsers(dest="command", required=True)

    _add_orgs_parser(sub_parsers)
    _add_repos_parser(sub_parsers)
    _add_contexts_parser(sub_parsers)

    args = parser.parse_args()

    try:
        args.func(args)
    except KnownError as ex:
        print(ex.args[0], file=sys.stderr)
        exit(1)


def _add_orgs_parser(sub_parsers):
    parser = sub_parsers.add_parser("orgs")
    parser.set_defaults(func=lambda _: cli.list_organizations())


def _add_repos_parser(sub_parsers):
    parser = sub_parsers.add_parser("repos")
    parser.add_argument("--org", help="The name of an organization")
    parser.set_defaults(func=lambda a: cli.list_repositories(a.org))

    sub_parsers = parser.add_subparsers(dest="repos_command", required=False)

    vars_parser = sub_parsers.add_parser("vars")
    vars_parser.add_argument("--org", dest="vars_org", help="The name of an organization")
    vars_parser.add_argument("--repo", help="The name of a repo")
    vars_parser.set_defaults(func=lambda a: cli.list_repositories_vars(
        a.org if a.vars_org is None else a.vars_org,
        a.repo
    ))


def _add_contexts_parser(sub_parsers):
    parser = sub_parsers.add_parser("contexts")
    parser.add_argument("--org", help="The name of an organization")
    parser.set_defaults(func=lambda a: cli.list_contexts(a.org))


if __name__ == "__main__":
    main()
