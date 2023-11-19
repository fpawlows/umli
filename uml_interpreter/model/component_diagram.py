from typing import Optional

import uml_interpreter.model.base_classes as bc
import uml_interpreter.model.class_diagram as cd


class ComponentDiagram(bc.StructuralDiagram):
    def __init__(self, name: str) -> None:
        super().__init__(name)
        self.components: list[Component] = []


class ComponentRelationMember:
    def __init__(self) -> None:
        self.relations_to: list[ComponentRelationship] = []
        self.relations_from: list[ComponentRelationship] = []


class ComponentRelationship:
    def __init__(
        self, source: ComponentRelationMember, target: ComponentRelationMember
    ) -> None:
        self.source = source
        source.relations_from.append(self)
        self.target = target
        target.relations_to.append(self)
        self.related_relationship: Optional[cd.ClassRelationship] = None


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
