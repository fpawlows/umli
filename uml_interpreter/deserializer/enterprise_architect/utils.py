from dataclasses import dataclass
from typing import Any

from uml_interpreter.model.diagrams.class_diagram import (
    ClassDiagramElement,
    ClassRelationship,
)
from abc import ABC, abstractmethod


class RelationshipEditor(ABC):
    def __init__(self, relationship: ClassRelationship) -> None:
        self._relationship = relationship

    @abstractmethod
    def __call__(self, *args: Any, **kwds: Any) -> ClassRelationship:
        pass


class SetRelationshipTarget(RelationshipEditor):
    def __call__(self, target: ClassDiagramElement) -> ClassRelationship:
        self._relationship.target = target
        return self._relationship


class SetRelationshipSource(RelationshipEditor):
    def __call__(self, source: ClassDiagramElement) -> ClassRelationship:
        self._relationship.source = source
        return self._relationship


@dataclass
class SourceDestinationPair:
    source: Any = None
    target: Any = None
