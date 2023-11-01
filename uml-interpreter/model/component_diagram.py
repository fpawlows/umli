from typing import Optional
from class_diagram import Element, ClassRelationship, Method
from base_classes import StructuralDiagram


class ComponentDiagram(StructuralDiagram):
    def __init__(self, name: str) -> None:
        super().__init__(name)
        self.components: list[Component] = []


class ComponentRelationMember():
    def __init__(self) -> None:
        self.relations_to: list[ComponentRelationship] = []
        self.relations_from: list[ComponentRelationship] = []


class ComponentRelationship():
    def __init__(self, source: ComponentRelationMember, target: ComponentRelationMember) -> None:
        self.source = source
        source.relations_from.append(self)
        self.target = target
        target.relations_to.append(self)
        self.related_relationship: Optional[ClassRelationship] = None


class Component(ComponentRelationMember):
    def __init__(self) -> None:
        super().__init__()
        self.children: list[Component] = []
        self.ports: list[Port] = []
        self.interfaces: list[ComponentInterface] = []
        self.elements: list[Element] = []
        self.name: str = ""


class Port(ComponentRelationMember):
    def __init__(self) -> None:
        super().__init__()
        self.interfaces: list[ComponentInterface] = []


class ComponentInterface(ComponentRelationMember):
    def __init__(self) -> None:
        super().__init__()
        self.methods = list[Method] = []
        self.name: str = ""


class ProvidedInterface(ComponentInterface):
    def __init__(self) -> None:
        super().__init__()
        self.fulfills: list[RequiredInterface] = []


class RequiredInterface(ComponentInterface):
    def __init__(self) -> None:
        super().__init__()
        self.fulfilled_by: list[ProvidedInterface] = []
