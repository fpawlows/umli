from abc import ABC


class UMLObject(ABC):
    def __init__(self, object_id: str = None) -> None:
        self._id = object_id or id(self)
        super().__init__()

    @property
    def id(self) -> str:
        return self._id

    @id.setter
    def id(self, new_id: str) -> None:
        self._id = new_id

