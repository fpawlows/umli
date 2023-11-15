from typing import Optional


class UMLModel:
    def __init__(self) -> None:
        self.diagrams: list[UMLDiagram] = []
        self.filename: Optional[str] = None


class UMLDiagram:
    def __init__(self, name: str) -> None:
        self.name = name


class StructuralDiagram(UMLDiagram):
    def __init__(self, name: str) -> None:
        super().__init__(name)


class BehavioralDiagram(UMLDiagram):
    def __init__(self, name: str) -> None:
        super().__init__(name)
