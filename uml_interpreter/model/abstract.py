from abc import ABC
from typing import Optional


class UMLObject(ABC):
    def __init__(self, object_id: Optional[str] = None) -> None:
        self._id = object_id
        super().__init__()

    @property
    def id(self) -> Optional[str]:
        return self._id

    @id.setter
    def id(self, new_id: str) -> None:
        self._id = new_id
