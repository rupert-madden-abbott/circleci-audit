from circleci_audit.circleci import CircleCiClient
from circleci_audit.config import load_config, ENV_VAR_PREFIX
from circleci_audit.repositories import RepositoryClient, Vcs


def validate_configuration():
    config = load_config()

    print("All required configuration provided")
    print(f"{ENV_VAR_PREFIX}TOKEN = REDACTED")
    print(f"{ENV_VAR_PREFIX}ORGANIZATION = {config.organization}")
    print(f"{ENV_VAR_PREFIX}VCS_NAME = {config.vcs_name}")
    print(f"{ENV_VAR_PREFIX}VCS_SLUG = {config.vcs_slug}")


def list_repositories():
    config = load_config()

    client = CircleCiClient(config.token)
    repository_client = RepositoryClient(client, Vcs(config.vcs_name, config.vcs_slug))

    for repository in repository_client.get_repositories(config.organization):
        print(f"{repository.name} {repository.url}")


