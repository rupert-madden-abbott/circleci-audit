from dataclasses import dataclass
from typing import Iterable, Dict, Any

from circleci_audit.circleci import CircleCiClient


@dataclass
class Vcs:
    name: str
    slug: str


@dataclass
class Repository:
    name: str
    url: str
    owner: str


class RepositoryClient:
    def __init__(self, client: CircleCiClient, vcs: Vcs):
        self.client = client
        self.vcs = vcs

    def get_repositories(self, owner: str) -> Iterable[Repository]:
        repositories = self.client.iterate_numbered_pages(f"/api/v1.1/user/repos/{self.vcs.name}")
        repositories = map(self._to_repository, repositories)
        return filter(lambda repo: repo.owner == owner, repositories)

    @staticmethod
    def _to_repository(item: Dict[str, Any]) -> Repository:
        return Repository(
            name=item.get("name"),
            url=item.get("vcs_url"),
            owner=item.get("owner").get("name")
        )
