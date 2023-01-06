import os
from dataclasses import dataclass

from circleci_audit.known_error import KnownError

ENV_VAR_PREFIX = "CIRCLECI_AUDIT_"
_DEFAULT_VCS_NAME = "github"
_DEFAULT_VCS_SLUG = "gh"


@dataclass
class Config:
    token: str


def load_config() -> Config:
    return Config(
        token=_load_env_var(f"{ENV_VAR_PREFIX}TOKEN")
    )


def _load_env_var(name: str, default: str = None) -> str:
    value = os.getenv(name, default)
    if value is None:
        raise KnownError(f"Missing required environment variable {name}")
    return value
