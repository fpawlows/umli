from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Any, Optional, Union

import uml_interpreter.model.diagrams.abstract as dg
import uml_interpreter.model.diagrams.sequence_diagram as sd
import uml_interpreter.visitor.model_visitor as v
from uml_interpreter.model.abstract import UMLObject
from uml_interpreter.model.errors import InvalidModelInitialization


class ClassDiagram(dg.StructuralDiagram):
    def __init__(self, name: Optional[str] = None, elements=None) -> None:
        super().__init__(name)
        self.elements: list[ClassDiagramElement] = elements or []

    def accept(self, visitor: v.ModelVisitor):
        visitor.visit_class_diagram(self)


class RelationshipType(Enum):
    """
    Enum representing Class Diagram relationships types.
    Values have to be strings to allow creation by calling
    RelationshipType(<name>)
    """

    Association = "Association"
    Generalization = "Generalization"


class ClassDiagramElement(sd.SequenceActor):
    def __init__(self, name: str) -> None:
        super().__init__(name)
        self.relations_to: list[ClassRelationship] = []
        self.relations_from: list[ClassRelationship] = []
        self.methods: list[ClassDiagramMethod] = []
        self.attributes: list[ClassDiagramAttribute] = []

    def accept(self, visitor: v.ModelVisitor) -> None:
        visitor.visit_class_diagram_element(self)

    def add_relationship_to(
        self,
        target_element: ClassDiagramElement,
        relation_type: Union[RelationshipType, str] = (
            RelationshipType.Association
        ),
        **rel_init_kwargs,
    ) -> ClassRelationship:
        """
        Adds relationship to a specified target. Accepts all key-word
        arguments supported by ClassRelationship
         initialization.

        :arg target_element - ClassDiagramElement instance, to which
            relationship should be created.
        :arg relation_type - RelationshipType enum instance or
            its string value, defining type of relationship
         to be created.

        """
        if target_element is None:
            raise InvalidModelInitialization(
                f"Couldn't add relationship to the class {str(self)}. "
                f"Target or created relationship must be specified"
            )

        if isinstance(relation_type, str):
            relation_type = RelationshipType(relation_type)

        relationship = ClassRelationship(
            source=self, target=target_element, type=relation_type,
            **rel_init_kwargs
        )
        return relationship

    def _add_to_relations_to(
        self, relationship: ClassRelationship
    ) -> ClassRelationship:
        """
        Adds relation to self.relations_to list.
        Logic unifying assignment of the element on relationship
        side is applied.

        :arg relationship - predefined ClassRelationship instance.
        During assignment its source side is set to
        the current element, but target side is left as given.
        """
        self.relations_to.append(relationship)
        relationship.source = self
        return relationship

    def set_as_source_of(self, relationship: ClassRelationship) -> (
            ClassRelationship
    ):
        """
        Set current ClassDiagramElement as a source side
          of the given relationship.
        Logic unifying assignment of the element on relationship
          side is applied.
        """
        relationship = self._add_to_relations_to(relationship)
        return relationship

    def add_relationship_from(
        self,
        source_element: ClassDiagramElement,
        relation_type: Union[RelationshipType, str] = (
            RelationshipType.Association
        ),
        **rel_init_kwargs,
    ) -> ClassRelationship:
        """
        Adds relationship from a specified target. Accepts all key-word
          arguments supported by ClassRelationship
         initialization.

        :arg source_element - ClassDiagramElement instance, from which
          relationship should be created.
        :arg relation_type - RelationshipType enum instance or its string
          value, defining type of relationship
         to be created.

        """
        if source_element is None:
            raise InvalidModelInitialization(
                f"Couldn't add relationship from the class {str(self)}. "
                f"Source or created relationship must be specified"
            )

        if isinstance(relation_type, str):
            relation_type = RelationshipType(relation_type)

        relationship = ClassRelationship(
            source=source_element, target=self, type=relation_type,
            **rel_init_kwargs
        )
        return relationship

    def _add_to_relations_from(
        self, relationship: ClassRelationship
    ) -> ClassRelationship:
        """
        Adds relation to self.relations_from list.
        Logic unifying assignment of the element on relationship side is
        applied.

        :arg relationship - predefined ClassRelationship instance. During
          assignment its source side is set to
        the current element, but target side is left as given.
        """
        self.relations_from.append(relationship)
        relationship.target = self
        return relationship

    def set_as_target_of(self, relationship: ClassRelationship) -> (
            ClassRelationship
            ):
        """
        Set current ClassDiagramElement as a target side of
        the given relationship.
        Logic unifying assignment of the element on relationship
        side is applied.
        """
        relationship = self._add_to_relations_from(relationship)
        return relationship


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


class ClassRelationship(UMLObject):
    @dataclass()
    class RelationshipSide:
        element: Optional[ClassDiagramElement] = None
        role: Optional[str] = None
        """
        Name of the property storing relationship on one side.
        """
        min_max_multiplicity: tuple[str, str] = ("0", "1")
        # TODO: change type to dataclass with values from enum with possible
        #  values (would be created from config with mapping of name
        # to python type (change name to multiplicity_range)
        # TODO: discuss default value

    def __init__(
        self,
        type: RelationshipType = RelationshipType.Association,
        name: Optional[str] = None,
        source: Optional[ClassDiagramElement] = None,
        target: Optional[ClassDiagramElement] = None,
        source_minmax: tuple[str, str] = ("0", "1"),
        target_minmax: tuple[str, str] = ("0", "1"),
        source_role: Optional[str] = None,
        target_role: Optional[str] = None,
        *,
        source_side: Optional[RelationshipSide] = None,
        target_side: Optional[RelationshipSide] = None,
        **kwargs,
    ) -> None:
        """
        Class representing UML Class Diagram Relationship between elements.

        :arg source_side - instance of ClassRelationship.RelationshipSide
            class. If specified, it has priority over other source-initializing
            arguments. Logic unifying assignment of the relationship on the
            source element side is applied - i.e. if given source_side's
            element doesn't have current relationship in its relations_to,
            it will be added.
        """
        self.source_side = source_side or ClassRelationship.RelationshipSide(
            source, source_role, source_minmax
        )
        self.target_side = target_side or ClassRelationship.RelationshipSide(
            target, target_role, target_minmax
        )

        self.type = type
        self.name = name
        super().__init__(**kwargs)

    @property
    def source_side(self) -> RelationshipSide:
        return self._source_side

    @property
    def source(self) -> Optional[ClassDiagramElement]:
        return self._source_side.element

    @source_side.setter
    def source_side(self, side: RelationshipSide) -> None:
        self._source_side = side
        if side.element is not None:
            """
            In case given side is a placeholder - not yet initialized.
            """
            side.element.set_as_source_of(self)

    @source.setter
    def source(self, new_source_element: ClassDiagramElement) -> None:
        if self.source is new_source_element:
            """
            Condition to avoid ciclic setters calls.
            """
            return

        if isinstance(new_source_element, ClassDiagramElement):
            self._source_side.element = new_source_element
            new_source_element.set_as_source_of(self)

        else:
            raise InvalidModelInitialization(
                f"Given class diagram element was not an instance "
                f"of defined class. New element: {str(new_source_element)}"
            )

    def create_source_side(
        self,
        source_element: ClassDiagramElement,
        role: Optional[str],
        min_max_multiplicity: Optional[tuple[str, str]],
    ) -> None:
        new_source_side = ClassRelationship.RelationshipSide(
            source_element, role, min_max_multiplicity or ("0", "1")
        )
        self.source_side = new_source_side

    @property
    def target_side(self) -> RelationshipSide:
        return self._target_side

    @property
    def target(self) -> Optional[ClassDiagramElement]:
        return self._target_side.element

    @target_side.setter
    def target_side(self, side: RelationshipSide) -> None:
        self._target_side = side
        if side.element is not None:
            """
            In case given side is a placeholder - not yet initialized.
            """
            side.element.set_as_target_of(self)

    @target.setter
    def target(self, new_target_element: ClassDiagramElement) -> None:
        if self.target is new_target_element:
            """
            Condition to avoid ciclic setters calls.
            """
            return

        if isinstance(new_target_element, ClassDiagramElement):
            self._target_side.element = new_target_element
            new_target_element.set_as_target_of(self)

        else:
            raise InvalidModelInitialization(
                f"Given class diagram element was not an instance of defined"
                f" class. New element: {str(new_target_element)}"
            )

    def create_target_side(
        self,
        target_element: ClassDiagramElement,
        role: Optional[str],
        min_max_multiplicity: Optional[tuple[str, str]],
    ) -> None:
        new_target_side = ClassRelationship.RelationshipSide(
            target_element, role, min_max_multiplicity or ("0", "1")
        )
        self.target_side = new_target_side

    def accept(self, visitor: v.ModelVisitor):
        visitor.visit_class_relationship(self)


class ClassDiagramMethod(UMLObject):
    def __init__(self, name: str, ret_type: str, parameters=None,
                 **kwargs) -> None:
        self.name = name
        self.parameters: list[ClassDiagramAttribute] = parameters or []
        self.ret_type = ret_type
        super().__init__(**kwargs)

    def accept(self, visitor: v.ModelVisitor):
        visitor.visit_diagram_method(self)


class ClassDiagramAttribute(UMLObject):
    def __init__(self, name: str, type: str, init_value: Any = None,
                 **kwargs) -> None:
        self.name = name
        self.type = type
        self.init_value = init_value
        super().__init__(**kwargs)

    def accept(self, visitor: v.ModelVisitor):
        visitor.visit_class_diagram_attribute(self)


class ClassDiagramMethodParameter(UMLObject):
    def __init__(
        self, name: Optional[str], type: str, default_value: Any = None,
            **kwargs) -> None:
        self.name = name or ""
        self.type = type
        self.default_value = default_value
        super().__init__(**kwargs)

    def accept(self, visitor: v.ModelVisitor):
        visitor.visit_class_diagram_method_parameter(self)
