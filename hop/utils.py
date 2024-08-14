from typing import Protocol

class Comparable(Protocol):
    def __lt__(self, other: "Comparable") -> bool:
        ...
