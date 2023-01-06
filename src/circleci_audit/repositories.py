from dataclasses import dataclass
from typing import Iterable, Dict, Any, Optional, List

from circleci_audit.circleci import CircleCiClient
from circleci_audit.organizations import Vcs


@dataclass
class Repository:
    name: str
    url: Optional[str]
    owner: str
    vcs_type: str


@dataclass
class Key:
    type: str
    fingerprint: str


class RepositoryClient:
    def __init__(self, client: CircleCiClient):
        self.client = client

    def get_repositories(self, vcs: Vcs, owner: Optional[str] = None) -> Iterable[Repository]:
        repositories = self.client.iterate_numbered_pages(f"/api/v1.1/user/repos/{vcs.name}")
        repositories = map(self._to_repository, repositories)

        if owner is not None:
            return filter(lambda repo: repo.owner == owner, repositories)
        else:
            return repositories

    def get_vars(self, repo: Repository) -> Iterable[str]:
        env_vars = self.client.iterate_unnumbered_pages(
            f"/api/v2/project/{repo.vcs_type}/{repo.owner}/{repo.name}/envvar")
        return map(lambda var: var["name"], env_vars)

    def get_keys(self, repo: Repository) -> List[Key]:
        keys = self.client.iterate_unnumbered_pages(
            f"/api/v2/project/{repo.vcs_type}/{repo.owner}/{repo.name}/checkout-key")
        keys = map(self._to_key, keys)
        keys = list(keys)
        settings = self._get_settings(repo)
        ssh_keys = settings["ssh_keys"]
        for ssh_key in ssh_keys:
            keys.append(Key("ssh-key", ssh_key["fingerprint"]))
        return keys

    def is_configured_with_jira(self, repository: Repository) -> bool:
        settings = self._get_settings(repository)
        jira = settings.get("jira")

        if jira is None:
            return False

        lifecycle = jira.get("lifecycle")

        if lifecycle == "installed":
            return True

        raise RuntimeError(f"Unknown lifecycle {lifecycle}")

    def _get_settings(self, repo: Repository):
        return self.client.get(
            f"https://circleci.com/api/v1.1/project/{repo.vcs_type}/{repo.owner}/{repo.name}/settings")

    @staticmethod
    def _to_repository(item: Dict[str, Any]) -> Repository:
        return Repository(
            name=item["name"],
            url=item["vcs_url"],
            owner=item["owner"]["name"],
            vcs_type=item["vcs_type"]
        )

    @staticmethod
    def _to_key(item: Dict[str, Any]) -> Key:
        return Key(
            type=item["type"],
            fingerprint=item["fingerprint"]
        )
