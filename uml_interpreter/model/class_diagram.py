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
        source: ClassDiagramElement | None = None,
        target: ClassDiagramElement | None = None,
    ) -> None:
        self.source = source
        if isinstance(source, ClassDiagramElement):
            source.relations_from.append(self)
        self.target = target
        if isinstance(target, ClassDiagramElement):
            target.relations_to.append(self)
        self.type = type

    def accept(self, visitor: v.ModelVisitor):
        visitor.visit_class_relationship(self)


class ClassDiagramMethod:
    def __init__(self, element: ClassDiagramElement, name: str, ret_type: str) -> None:
        self.assigned_element = element
        element.methods.append(self)
        self.name = name
        self.attributes: list[ClassDiagramAttribute] = []
        self.ret_type = ret_type

    def accept(self, visitor: v.ModelVisitor):
        visitor.visit_diagram_method(self)


class ClassDiagramAttribute:
    def __init__(
        self, element: ClassDiagramElement | ClassDiagramMethod, name: str, type: str
    ) -> None:
        self.assigned_element = element
        element.attributes.append(self)
        self.name = name
        self.type = type

    def accept(self, visitor: v.ModelVisitor):
        visitor.visit_class_diagram_attribute(self)
