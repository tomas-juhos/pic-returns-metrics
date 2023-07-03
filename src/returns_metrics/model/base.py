"""Abstract model."""

from abc import ABC, abstractmethod
from typing import Dict, List, Tuple


class Modeling(ABC):
    """Modeling abstract class."""

    @classmethod
    @abstractmethod
    def build_record(cls, key: List, returns: List[Tuple[Dict, float]]) -> "Modeling":
        """Transforms record into record object.

        Args:
            key: object key.
            returns: list of returns for the key.
        Returns:
            Record object for the given entity.
        """

    @abstractmethod
    def as_tuple(self) -> Tuple:
        """Returns object values as a tuple.

        Returns:
            Record object attributes as a tuple.
        """
