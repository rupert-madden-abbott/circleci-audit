from dataclasses import dataclass
from typing import Iterable, Dict, Any

from circleci_audit.circleci import CircleCiClient


@dataclass
class Context:
    id: str
    name: str


class ContextClient:
    def __init__(self, client: CircleCiClient):
        self.client = client

    def get_contexts(self, owner_id: str) -> Iterable[Context]:
        contexts = self.client.iterate_unnumbered_pages(f"/api/v2/context", {"owner-id": owner_id})
        return map(self._to_context, contexts)

    @staticmethod
    def _to_context(item: Dict[str, Any]) -> Context:
        return Context(
            id=item["id"],
            name=item["name"]
        )
