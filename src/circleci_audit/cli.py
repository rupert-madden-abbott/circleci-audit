from typing import Optional, Iterable

from circleci_audit.circleci import CircleCiClient, HttpError
from circleci_audit.config import load_config
from circleci_audit.contexts import ContextClient
from circleci_audit.known_error import KnownError
from circleci_audit.organizations import OrganizationClient
from circleci_audit.repositories import RepositoryClient, Repository


def list_organizations():
    config = load_config()
    client = _get_organizations_client(config)

    for organization in client.get_organizations():
        print(f"{organization.name} {organization.vcs_type}")


def list_repositories(org: Optional[str]):
    config = load_config()
    org_client = _get_organizations_client(config)
    repo_client = _get_repository_client(config)

    if org is not None:
        for repository in _get_org_repositories(org_client, repo_client, org):
            print(f"{repository.name} {repository.url}")
    else:
        for repository in _get_repositories(org_client, repo_client):
            print(f"{repository.owner} {repository.name} {repository.url}")


def list_repositories_vars(org: Optional[str], repo: Optional[str]):
    config = load_config()
    org_client = _get_organizations_client(config)
    repo_client = _get_repository_client(config)

    if org is None:
        for repository in _get_repositories(org_client, repo_client):
            for env_var in _get_vars(repo_client, repository):
                print(f"{repository.owner} {repository.name} {env_var}")
    elif repo is None:
        for repository in _get_org_repositories(org_client, repo_client, org):
            for env_var in _get_vars(repo_client, repository):
                print(f"{repository.name} {env_var}")
    else:
        organization = _get_organization(org_client, org)
        for env_var in _get_vars(repo_client, Repository(repo, None, org, organization.vcs_type)):
            print(f"{env_var}")


def _get_vars(repo_client: RepositoryClient, repository: Repository) -> Iterable[str]:
    repositories = repo_client.get_vars(repository)
    while True:
        try:
            yield next(repositories)
        except StopIteration:
            break
        except HttpError as ex:
            if ex.response.status == 404:
                return []
            raise


def list_contexts(org_name: Optional[str]):
    config = load_config()
    org_client = _get_organizations_client(config)
    context_client = _get_contexts_client(config)

    if org_name is not None:
        organization = _get_organization(org_client, org_name)
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


def _get_repository_client(config) -> RepositoryClient:
    client = CircleCiClient(config.token)
    return RepositoryClient(client)


def _get_repositories(org_client: OrganizationClient, repo_client: RepositoryClient) -> Iterable[Repository]:
    organizations = org_client.get_organizations()
    vcss = set(map(lambda o: o.vcs(), organizations))
    for vcs in vcss:
        for repository in repo_client.get_repositories(vcs):
            yield repository


def _get_org_repositories(
        org_client: OrganizationClient,
        repo_client: RepositoryClient,
        org: str
) -> Iterable[Repository]:
    organization = _get_organization(org_client, org)
    return repo_client.get_repositories(organization.vcs(), org)


def _get_organization(org_client: OrganizationClient, org: str):
    organization = org_client.get_organization(org)
    if organization is None:
        raise KnownError(f"No organisation found with name {org}")
    return organization
