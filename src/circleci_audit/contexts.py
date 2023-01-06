from dataclasses import dataclass
from typing import Iterable, Dict, Any, Optional

from circleci_audit.circleci import CircleCiClient
from circleci_audit.organizations import Organization


@dataclass
class Context:
    id: Optional[str]
    name: str
    owner: str


class ContextClient:
    def __init__(self, client: CircleCiClient):
        self.client = client

    def get_contexts(self, organization: Organization) -> Iterable[Context]:
        contexts = self.client.iterate_unnumbered_pages(f"/api/v2/context", {"owner-id": organization.id})
        return map(lambda c: self._to_context(organization, c), contexts)

    def get_context(self, organization: Organization, name: str) -> Context:
        contexts = self.get_contexts(organization)
        return next(iter(context for context in contexts if context.name == name), None)

    def get_vars(self, context: Context) -> Iterable[str]:
        env_vars = self.client.iterate_unnumbered_pages(f"/api/v2/context/{context.id}/environment-variable")
        return map(lambda var: var["variable"], env_vars)

    @staticmethod
    def _to_context(organization: Organization, item: Dict[str, Any]) -> Context:
        return Context(
            id=item["id"],
            name=item["name"],
            owner=organization.name
        )
