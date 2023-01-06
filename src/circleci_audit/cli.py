from typing import Optional

from circleci_audit.circleci import CircleCiClient
from circleci_audit.config import load_config
from circleci_audit.contexts import ContextClient
from circleci_audit.known_error import KnownError
from circleci_audit.organizations import OrganizationClient
from circleci_audit.repositories import RepositoryClient


def list_organizations():
    config = load_config()
    client = _get_organizations_client(config)

    for organization in client.get_organizations():
        print(f"{organization.name} {organization.vcs_type}")


def list_repositories(org_name: Optional[str]):
    config = load_config()
    org_client = _get_organizations_client(config)
    repo_client = _get_repository_client(config)

    if org_name is not None:
        organization = org_client.get_organization(org_name)
        if organization is None:
            raise KnownError(f"No organisation found with name {org_name}")

        for repository in repo_client.get_repositories(organization.vcs(), org_name):
            print(f"{repository.name} {repository.url}")
    else:
        organizations = org_client.get_organizations()
        vcss = set(map(lambda org: org.vcs(), organizations))

        for vcs in vcss:
            for repository in repo_client.get_repositories(vcs):
                print(f"{repository.owner} {repository.name} {repository.url}")


def list_contexts(org_name: Optional[str]):
    config = load_config()
    org_client = _get_organizations_client(config)
    context_client = _get_contexts_client(config)

    if org_name is not None:
        organization = org_client.get_organization(org_name)
        if organization is None:
            raise KnownError(f"No organisation found with name {org_name}")

        for context in context_client.get_contexts(organization.id):
            print(f"{context.name}")
    else:
        organizations = org_client.get_organizations()
        for organization in organizations:
            if organization.id is not None:
                for context in context_client.get_contexts(organization.id):
                    print(f"{organization.name} {context.name}")


def _get_contexts_client(config) -> ContextClient:
    client = CircleCiClient(config.token)
    return ContextClient(client)


def _get_organizations_client(config) -> OrganizationClient:
    client = CircleCiClient(config.token)
    return OrganizationClient(client)


def _get_repository_client(config):
    client = CircleCiClient(config.token)
    return RepositoryClient(client)
