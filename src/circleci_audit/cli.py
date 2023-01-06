from typing import Optional, Iterable, List

from circleci_audit.circleci import CircleCiClient, HttpError
from circleci_audit.config import load_config
from circleci_audit.contexts import ContextClient, Context
from circleci_audit.known_error import KnownError
from circleci_audit.organizations import OrganizationClient
from circleci_audit.repositories import RepositoryClient, Repository, Key


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
            for env_var in _get_repo_vars(repo_client, repository):
                print(f"{repository.owner} {repository.name} {env_var}")
    elif repo is None:
        for repository in _get_org_repositories(org_client, repo_client, org):
            for env_var in _get_repo_vars(repo_client, repository):
                print(f"{repository.name} {env_var}")
    else:
        organization = _get_organization(org_client, org)
        for env_var in _get_repo_vars(repo_client, Repository(repo, None, org, organization.vcs_type)):
            print(f"{env_var}")


def list_repositories_keys(org: Optional[str], repo: Optional[str]):
    config = load_config()
    org_client = _get_organizations_client(config)
    repo_client = _get_repository_client(config)

    if org is None:
        for repository in _get_repositories(org_client, repo_client):
            for key in _get_repo_keys(repo_client, repository):
                print(f"{repository.owner} {repository.name} {key.type} {key.fingerprint}")
    elif repo is None:
        for repository in _get_org_repositories(org_client, repo_client, org):
            for key in _get_repo_keys(repo_client, repository):
                print(f"{repository.name} {key.type} {key.fingerprint}")
    else:
        organization = _get_organization(org_client, org)
        for key in _get_repo_keys(repo_client, Repository(repo, None, org, organization.vcs_type)):
            print(f"{key.type} {key.fingerprint}")


def list_repositories_jira(org: Optional[str]):
    config = load_config()
    org_client = _get_organizations_client(config)
    repo_client = _get_repository_client(config)

    if org is None:
        for repository in _get_repositories(org_client, repo_client):
            if _repo_is_configured_with_jira(repo_client, repository):
                print(f"{repository.owner} {repository.name}")
    else:
        for repository in _get_org_repositories(org_client, repo_client, org):
            if _repo_is_configured_with_jira(repo_client, repository):
                print(f"{repository.name}")


def list_contexts(org_name: Optional[str]):
    config = load_config()
    org_client = _get_organizations_client(config)
    context_client = _get_contexts_client(config)

    if org_name is not None:
        for context in _get_org_contexts(org_client, context_client, org_name):
            print(f"{context.name}")
    else:
        for context in _get_contexts(org_client, context_client):
            print(f"{context.owner} {context.name}")


def list_context_vars(org: Optional[str], context: Optional[str]):
    config = load_config()
    org_client = _get_organizations_client(config)
    context_client = _get_contexts_client(config)

    if org is None:
        for context in _get_contexts(org_client, context_client):
            for env_var in context_client.get_vars(context):
                print(f"{context.owner} {context.name} {env_var}")
    elif context is None:
        for context in _get_org_contexts(org_client, context_client, org):
            for env_var in context_client.get_vars(context):
                print(f"{context.name} {env_var}")
    else:
        organization = _get_organization(org_client, org)
        context = context_client.get_context(organization, context)
        if context is None:
            raise KnownError(f"No context found with name {context}")
        for env_var in context_client.get_vars(context):
            print(f"{env_var}")


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


def _get_contexts(org_client: OrganizationClient, context_client: ContextClient) -> Iterable[Context]:
    organizations = org_client.get_organizations()
    for organization in organizations:
        if organization.id is not None:
            for context in context_client.get_contexts(organization):
                yield context


def _get_org_contexts(
        org_client: OrganizationClient,
        context_client: ContextClient,
        org: str
) -> Iterable[Context]:
    organization = _get_organization(org_client, org)
    return context_client.get_contexts(organization)


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


def _get_repo_vars(repo_client: RepositoryClient, repository: Repository) -> Iterable[str]:
    env_vars = repo_client.get_vars(repository)
    while True:
        try:
            yield next(env_vars)
        except StopIteration:
            break
        except HttpError as ex:
            if ex.response.status == 404:
                return []
            raise


def _get_repo_keys(repo_client: RepositoryClient, repository: Repository) -> List[Key]:
    try:
        return repo_client.get_keys(repository)
    except HttpError as ex:
        if ex.response.status == 404:
            return []
        raise


def _repo_is_configured_with_jira(repo_client: RepositoryClient, repository: Repository) -> bool:
    try:
        return repo_client.is_configured_with_jira(repository)
    except HttpError as ex:
        if ex.response.status == 404:
            return False
        raise
