from typing import Any

import uml_interpreter.model.base_classes as bc
import uml_interpreter.model.sequence_diagram as sd
import uml_interpreter.visitor.visitor as v


class ClassDiagram(bc.StructuralDiagram):
    def __init__(self, name: str, elements=None) -> None:
        super().__init__(name)
        self.elements: list[ClassDiagramElement] = elements if elements else []

    def accept(self, visitor: v.ModelVisitor):
        visitor.visit_class_diagram(self)


class ClassDiagramElement(sd.SequenceActor):
    def __init__(self, name: str) -> None:
        super().__init__(name)
        self.relations_to: list[ClassRelationship] = []
        self.relations_from: list[ClassRelationship] = []
        self.methods: list[ClassDiagramMethod] = []
        self.attributes: list[ClassDiagramAttribute] = []

    def accept(self, visitor: v.ModelVisitor):
        visitor.visit_class_diagram_element(self)


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
    def __init__(
        self,
        type: str,
        source_role: str | None,
        target_role: str | None,
        source_minmax: tuple[str, str] = ("", ""),
        target_minmax: tuple[str, str] = ("", ""),
        source: ClassDiagramElement | None = None,
        target: ClassDiagramElement | None = None,
    ) -> None:
        self.source = source
        self.source_role = source_role if source_role else ""
        self.source_minmax = source_minmax
        if isinstance(source, ClassDiagramElement):
            source.relations_from.append(self)

        self.target = target
        self.target_role = target_role if target_role else ""
        self.target_minmax = target_minmax
        if isinstance(target, ClassDiagramElement):
            target.relations_to.append(self)

        self.type = type

    def accept(self, visitor: v.ModelVisitor):
        visitor.visit_class_relationship(self)


class ClassDiagramMethod:
    def __init__(self, name: str, ret_type: str, parameters=None) -> None:
        self.name = name
        self.parameters: list[ClassDiagramAttribute] = parameters if parameters else []
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
    def __init__(self, name: str, type: str, default_value: Any = None) -> None:
        self.name = name
        self.type = type
        self.default_value = default_value

    def accept(self, visitor: v.ModelVisitor):
        visitor.visit_class_diagram_method_parameter(self)
