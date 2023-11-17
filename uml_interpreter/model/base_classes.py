from typing import Optional


class UMLModel:
    def __init__(self, diagrams=None, filename=None) -> None:
        self.diagrams: list[UMLDiagram] = diagrams if diagrams else []
        self.filename: Optional[str] = filename


class UMLDiagram:
    def __init__(self, name: str) -> None:
        self.name = name


class StructuralDiagram(UMLDiagram):
    def __init__(self, name: str) -> None:
        super().__init__(name)


class BehavioralDiagram(UMLDiagram):
    def __init__(self, name: str) -> None:
        super().__init__(name)
