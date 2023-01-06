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

    keys_parser = sub_parsers.add_parser("keys")
    keys_parser.add_argument("--org", dest="keys_org", help="The name of an organization")
    keys_parser.add_argument("--repo", help="The name of a repo")
    keys_parser.set_defaults(func=lambda a: cli.list_repositories_keys(
        a.org if a.keys_org is None else a.keys_org,
        a.repo
    ))

    jira_parser = sub_parsers.add_parser("jira")
    jira_parser.add_argument("--org", dest="jira_org", help="The name of an organization")
    jira_parser.set_defaults(func=lambda a: cli.list_repositories_jira(
        a.org if a.jira_org is None else a.jira_org
    ))


def _add_contexts_parser(sub_parsers):
    parser = sub_parsers.add_parser("contexts")
    parser.add_argument("--org", help="The name of an organization")
    parser.set_defaults(func=lambda a: cli.list_contexts(a.org))

    sub_parsers = parser.add_subparsers(dest="contexts_command", required=False)

    vars_parser = sub_parsers.add_parser("vars")
    vars_parser.add_argument("--org", dest="vars_org", help="The name of an organization")
    vars_parser.add_argument("--context", help="The name of a context")
    vars_parser.set_defaults(func=lambda a: cli.list_context_vars(
        a.org if a.vars_org is None else a.vars_org,
        a.context
    ))

if __name__ == "__main__":
    main()
