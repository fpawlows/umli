from typing import Optional

from uml_interpreter.visitor.model_visitor import ModelVisitor
from uml_interpreter.model.abstract import UMLObject


class UMLDiagram(UMLObject):
    def __init__(self, name: Optional[str] = None, **kwargs) -> None:
        self.name: str = name or ""
        super().__init__(**kwargs)

    def accept(self, visitor: ModelVisitor):
        visitor.visit_diagram(self)


class StructuralDiagram(UMLDiagram):
    def __init__(self, name: Optional[str] = None) -> None:
        super().__init__(name)


class BehavioralDiagram(UMLDiagram):
    def __init__(self, name: Optional[str] = None) -> None:
        super().__init__(name)
