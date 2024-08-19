from abc import abstractmethod
from typing import Protocol

class Comparable(Protocol):
    @abstractmethod
    def __lt__(self, other: "Comparable") -> bool: ...
