from sequence_diagram import Actor
from base_classes import StructuralDiagram


class ClassDiagram(StructuralDiagram):
    def __init__(self, name: str) -> None:
        super().__init__(name)
        self.elements: list[Element] = []


class Element(Actor):
    def __init__(self, name: str) -> None:
        super().__init__(name)
        self.relations_to: list[ClassRelationship] = []
        self.relations_from: list[ClassRelationship] = []
        self.methods: list[Method] = []


class ClassElement(Element):
    def __init__(self, name: str) -> None:
        super().__init__(name)


class InterfaceElement(Element):
    def __init__(self, name: str) -> None:
        super().__init__(name)


class ClassRelationship():
    def __init__(self, source: Element, target: Element) -> None:
        self.source = source
        source.relations_from.append(self)
        self.target = target
        target.relations_to.append(self)


class Method():
    def __init__(self, element: Element, name: str) -> None:
        self.assigned_element = element
        element.methods.append(self)
        self.name = name
