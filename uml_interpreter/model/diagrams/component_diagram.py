from typing import Optional

import uml_interpreter.model.diagrams.abstract as dg
import uml_interpreter.model.diagrams.class_diagram as cd
from uml_interpreter.model.abstract import UMLObject


class ComponentDiagram(dg.StructuralDiagram):
    def __init__(self, name: str) -> None:
        super().__init__(name)
        self.components: list[Component] = []


class ComponentRelationMember(UMLObject):
    def __init__(self, **kwargs) -> None:
        self.relations_to: list[ComponentRelationship] = []
        self.relations_from: list[ComponentRelationship] = []
        super().__init__(**kwargs)


class ComponentRelationship(UMLObject):
    def __init__(
        self, source: ComponentRelationMember, target: ComponentRelationMember,
        **kwargs
    ) -> None:
        self.source = source
        source.relations_from.append(self)
        self.target = target
        target.relations_to.append(self)
        self.related_relationship: Optional[cd.ClassRelationship] = None
        super().__init__(**kwargs)


class Component(ComponentRelationMember):
    def __init__(self) -> None:
        super().__init__()
        self.children: list[Component] = []
        self.ports: list[Port] = []
        self.interfaces: list[ComponentInterface] = []
        self.elements: list[cd.ClassDiagramElement] = []
        self.name: str = ""


class Port(ComponentRelationMember):
    def __init__(self) -> None:
        super().__init__()
        self.interfaces: list[ComponentInterface] = []


class ComponentInterface(ComponentRelationMember):
    def __init__(self) -> None:
        super().__init__()
        self.methods: list[cd.ClassDiagramMethod] = []
        self.name: str = ""


class ProvidedComponentInterface(ComponentInterface):
    def __init__(self) -> None:
        super().__init__()
        self.fulfills: list[RequiredComponentInterface] = []


class RequiredComponentInterface(ComponentInterface):
    def __init__(self) -> None:
        super().__init__()
        self.fulfilled_by: list[ProvidedComponentInterface] = []
