from dataclasses import dataclass
from typing import Any, NamedTuple

from uml_interpreter.model.class_diagram import ClassDiagramElement, ClassRelationship
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


class ElemWithId(NamedTuple):
    elem: ClassDiagramElement | ClassRelationship | Any
    id: str


@dataclass
class RelIds:
    src_id: str
    dst_id: str


class RelWithIds(NamedTuple):
    rel: ClassRelationship
    ids: RelIds


@dataclass
class RelEndRoles:
    src_role: str
    dst_role: str


class EndMinMax(NamedTuple):
    min: str
    max: str


@dataclass
class RelEndsMinMax:
    src_minmax: EndMinMax
    dst_minmax: EndMinMax
