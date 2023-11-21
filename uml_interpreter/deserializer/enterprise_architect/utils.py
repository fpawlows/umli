from dataclasses import dataclass
from typing import Any, NamedTuple

from uml_interpreter.model.class_diagram import ClassDiagramElement, ClassRelationship


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
