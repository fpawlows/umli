from typing import Any, Optional
from dataclasses import dataclass

import uml_interpreter.model.base_classes as bc
import uml_interpreter.model.sequence_diagram as sd
import uml_interpreter.visitor.model_visitor as v


class ClassDiagram(bc.StructuralDiagram):
    def __init__(self, name: Optional[str] = None, elements=None) -> None:
        super().__init__(name)
        self.elements: list[ClassDiagramElement] = elements or []

    def accept(self, visitor: v.ModelVisitor):
        visitor.visit_class_diagram(self)


class ClassDiagramElement(sd.SequenceActor):
    def __init__(self, name: str) -> None:
        super().__init__(name)
        self.relations_to: list[ClassRelationship] = []
        self.relations_from: list[ClassRelationship] = []
        self.methods: list[ClassDiagramMethod] = []
        self.attributes: list[ClassDiagramAttribute] = []

    def accept(self, visitor: v.ModelVisitor) -> None:
        visitor.visit_class_diagram_element(self)

    def add_relationship_to(self, relationship) -> None:
        self.relations_to.append(relationship)
        relationship.source = self

    def add_relationship_from(self, relationship) -> None:
        self.relations_from.append(relationship)
        relationship.target = self


class ClassDiagramClass(ClassDiagramElement):
    def __init__(self, name: str) -> None:
        super().__init__(name)

    def accept(self, visitor: v.ModelVisitor):
        visitor.visit_class_diagram_class(self)


class ClassDiagramInterface(ClassDiagramElement):
    def __init__(self, name: str) -> None:
        super().__init__(name)

    def accept(self, visitor: v.ModelVisitor):
        visitor.visit_class_diagram_interface(self)


class ClassRelationship:

    @dataclass
    class RelationshipSide:
        element: ClassDiagramElement
        role: Optional[str] = ""
        # TODO: change na default None else remove Optional
        # TODO: enum

        min_max_multiplicity: tuple[str, str] = ("0", "*")
        # TODO: change to dataclass with values from enum (change name to multiplicity)
        # TODO: ask why empty strings - not Nones + separate class?
        # TODO: discuss default value

        # TODO: discuss if we need setters
        # self.source_role = source_role or ""
        # self.source_minmax = source_minmax
        # self.target_role = target_role or ""
        # self.target_minmax = target_minmax

    def __init__(
        self,
        type: str,
        name: str,
        # TODO: discuss below default values -> to None if Optional
        source_role: Optional[str] = "",
        target_role: Optional[str] = "",
        source_minmax: tuple[str, str] = ("", ""),
        target_minmax: tuple[str, str] = ("", ""),
        source: Optional[ClassDiagramElement] = None,
        target: Optional[ClassDiagramElement] = None,
    ) -> None:
        self._source_side = ClassRelationship.RelationshipSide(source, source_role, source_minmax)
        self._target_side = ClassRelationship.RelationshipSide(target, target_role, target_minmax)

        self.type = type
        # TODO: make enum
        self.name = name

    @property
    def source_side(self) -> RelationshipSide:
        return self._source_side

    @property
    def source(self) -> ClassDiagramElement:
        return self._source_side.element

    @source_side.setter
    def source_side(self, side: RelationshipSide) -> None:
        self._source_side = side
        side.element.add_relationship_to(self)

    @source.setter
    def source(self, new_source_element: ClassDiagramElement) -> None:
        if self.source is new_source_element:
            """
            Condition to avoid ciclic setters calls.
            TODO: is there some pattern for such case"""
            return

        if isinstance(new_source_element, ClassDiagramElement):
            # TODO: should it erase previous multiplicity and role?
            self._source_side.element = new_source_element
            new_source_element.add_relationship_to(self)

        else:
            """
            TODO: raise custom exception """

    def create_source_side(self, source_element: ClassDiagramElement, role: Optional[str], min_max_multiplicity: Optional[tuple[str, str]]) -> None:
        new_source_side = ClassRelationship.RelationshipSide(source_element, role, min_max_multiplicity)
        self.source_side = new_source_side

    @property
    def target_side(self) -> RelationshipSide:
        return self._target_side

    @property
    def target(self) -> ClassDiagramElement:
        return self._target_side.element

    @target_side.setter
    def target_side(self, side: RelationshipSide) -> None:
        self._target_side = side
        side.element.add_relationship_from(self)

    @target.setter
    def target(self, new_target_element: ClassDiagramElement) -> None:
        if self.target is new_target_element:
            """
            Condition to avoid ciclic setters calls.
            TODO: is there some pattern for such case"""
            return

        if isinstance(new_target_element, ClassDiagramElement):
            # TODO: should it erase previous multiplicity and role?
            self._target_side.element = new_target_element
            new_target_element.add_relationship_from(self)

        else:
            """
            TODO: raise custom exception """

    def create_target_side(self, target_element: ClassDiagramElement, role: Optional[str], min_max_multiplicity: Optional[tuple[str, str]]) -> None:
        new_target_side = ClassRelationship.RelationshipSide(target_element, role, min_max_multiplicity)
        self.target_side = new_target_side

    def accept(self, visitor: v.ModelVisitor):
        visitor.visit_class_relationship(self)


class ClassDiagramMethod:
    def __init__(self, name: str, ret_type: str, parameters=None) -> None:
        self.name = name
        self.parameters: list[ClassDiagramAttribute] = parameters or []
        self.ret_type = ret_type

    def accept(self, visitor: v.ModelVisitor):
        visitor.visit_diagram_method(self)


class ClassDiagramAttribute:
    def __init__(self, name: str, type: str, init_value: Any = None) -> None:
        self.name = name
        self.type = type
        self.init_value = init_value

    def accept(self, visitor: v.ModelVisitor):
        visitor.visit_class_diagram_attribute(self)


class ClassDiagramMethodParameter:
    def __init__(self, name: Optional[str], type: str, default_value: Any = None) -> None:
        self.name = name or ""
        self.type = type
        self.default_value = default_value

    def accept(self, visitor: v.ModelVisitor):
        visitor.visit_class_diagram_method_parameter(self)
