from dataclasses import dataclass
from typing import Dict, Any, Optional, Iterable

from circleci_audit.circleci import CircleCiClient


@dataclass(frozen=True, eq=True)
class Vcs:
    name: str
    slug: str


GITHUB_VCS = Vcs("github", "gh")
BITBUCKET_VCS = Vcs("bitbucket", "bb")


@dataclass
class Organization:
    id: Optional[str]
    name: str
    slug: str
    vcs_type: str

    def vcs(self) -> Vcs:
        if self.vcs_type == "github":
            return GITHUB_VCS
        elif self.vcs_type == "bitbucket":
            return BITBUCKET_VCS
        else:
            raise RuntimeError(f"Unknown VCS type {self.vcs_type} for organization {self.name}")


class OrganizationClient:
    def __init__(self, client: CircleCiClient):
        self.client = client

    def get_organizations(self) -> Iterable[Organization]:
        organizations = self.client.get("/api/v2/me/collaborations")
        return map(self._to_organization, organizations)

    def get_organization(self, name: str) -> Optional[Organization]:
        organizations = self.get_organizations()
        return next(iter(org for org in organizations if org.name == name), None)

    @staticmethod
    def _to_organization(item: Dict[str, Any]) -> Organization:
        return Organization(
            id=item["id"],
            name=item["name"],
            slug=item["slug"],
            vcs_type=item["vcs_type"]
        )
