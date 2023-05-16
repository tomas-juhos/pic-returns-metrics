"""Entity file."""

from enum import Enum


class Entity(str, Enum):
    """Entities."""

    PORTFOLIO_METRICS = "PORTFOLIO_METRICS"
    METRICS = "METRICS"

    def __repr__(self) -> str:
        return str(self.value)
