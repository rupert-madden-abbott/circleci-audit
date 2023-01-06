from dataclasses import dataclass
from typing import Iterable, Dict, Any, Optional

from circleci_audit.circleci import CircleCiClient
from circleci_audit.organizations import Vcs


@dataclass
class Repository:
    name: str
    url: Optional[str]
    owner: str
    vcs_type: str


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

    @staticmethod
    def _to_repository(item: Dict[str, Any]) -> Repository:
        return Repository(
            name=item["name"],
            url=item["vcs_url"],
            owner=item["owner"]["name"],
            vcs_type=item["vcs_type"]
        )
