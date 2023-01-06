from dataclasses import dataclass
from typing import Iterable, Dict, Any, Optional

from circleci_audit.circleci import CircleCiClient
from circleci_audit.organizations import Vcs


@dataclass
class Repository:
    name: str
    url: str
    owner: str


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

    @staticmethod
    def _to_repository(item: Dict[str, Any]) -> Repository:
        return Repository(
            name=item["name"],
            url=item["vcs_url"],
            owner=item["owner"]["name"]
        )
