from typing import Optional

from uml_interpreter.visitor.model_visitor import ModelPrinter, ModelVisitor
from uml_interpreter.model.diagrams.abstract import UMLDiagram
from uml_interpreter.model.abstract import UMLObject

class UMLModel(UMLObject):
    def __init__(self, diagrams=None, filename=None) -> None:
        self.diagrams: list[UMLDiagram] = diagrams or []
        self.filename: Optional[str] = filename

    def accept(self, visitor: ModelVisitor):
        visitor.visit_model(self)

    def print(self, indent: int = 0, indent_inc: int = 2):
        self.accept(ModelPrinter(indent, indent_inc))
