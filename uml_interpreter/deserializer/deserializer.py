import xml.etree.ElementTree as ET
from typing import Optional

from uml_interpreter.deserializer.constants import EA_ATTR, EA_TAGS
from uml_interpreter.model.base_classes import UMLDiagram, UMLModel
from uml_interpreter.model.class_diagram import (ClassDiagram,
                                                 ClassDiagramClass,
                                                 ClassDiagramElement)
from uml_interpreter.source.source import Source


class InvalidXMLError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return f"Parser Error: {self.msg}"


class Deserializer:
    def __init__(self, source: Source) -> None:
        self.source = source

    def parse(self) -> UMLModel:  # type: ignore
        pass


class XMLDeserializer(Deserializer):
    def __init__(self, source: Source) -> None:
        super().__init__(source)
        self.curr_elem: Optional[ClassDiagramElement] = None

    def parse(self) -> UMLModel:
        try:
            tree: ET.ElementTree = self.source.read()
            return self.parse_model(tree)
        except ET.ParseError as exc:
            raise InvalidXMLError(exc.msg)

    def parse_model(self, tree: ET.ElementTree) -> UMLModel:  # type: ignore
        pass


class EnterpriseArchitectXMLDeserializer(XMLDeserializer):
    def __init__(self, source: Source) -> None:
        super().__init__(source)

    def parse_model(self, tree: ET.ElementTree) -> UMLModel:
        root = tree.getroot()
        if not isinstance(root, ET.Element):
            raise InvalidXMLError("No root node found in the XML file")

        model = root.find(EA_TAGS["model"])
        if model is None:
            raise InvalidXMLError("No model node found in the XML file")

        elems: list[tuple[ClassDiagramElement, str]] = self.parse_elems(
            root
        )  # TODO other diagrams

        diagrams: list[UMLDiagram] = self.parse_diagrams(root, elems)

        model = UMLModel()
        model.diagrams = diagrams

        return model

    def parse_elems(self, model: ET.Element) -> list[tuple[ClassDiagramElement, str]]:
        elems: list[tuple[ClassDiagramElement, str]] = []

        for elem in model.iter(EA_TAGS["elem"]):
            elems.append(self.parse_elem(elem))

        return elems

    def parse_elem(self, elem: ET.Element) -> tuple[ClassDiagramElement, str]:
        if self.try_build_class(elem) or self.try_build_relationship(elem):
            elem_id = elem.attrib[EA_ATTR["elem_id"]]
            if elem_id is None:
                raise InvalidXMLError("UML Model element is missing an id!")
            return (self.curr_elem, elem_id)

    def parse_diagrams(
        self, root: ET.Element, elems: list[tuple[ClassDiagramElement, str]]
    ) -> list[UMLDiagram]:
        diagrams: list[UMLDiagram] = []

        ext = root.find(EA_TAGS["ext"])
        if ext is None:
            raise InvalidXMLError("No Extension node found in the XML file")

        diags = ext.find(EA_TAGS["diags"])
        if diags is None:
            raise InvalidXMLError("No diagrams found in the XML file")

        for diag in diags.iter(EA_TAGS["diag"]):
            diagrams.append(self.assign_elems(diag, elems))

        return diagrams

    def assign_elems(
        self, diag: ET.Element, elems: list[tuple[ClassDiagramElement, str]]
    ) -> UMLDiagram:
        # Placeholder - just to see if the parser works
        diag_elems = diag.find(EA_TAGS["diag_elems"])
        if diag_elems is None:
            return UMLDiagram("placeholder")

        diag_type: str = "unknown"
        elem_ids: list[str] = []

        for diag_elem in diag_elems.iter(EA_TAGS["diag_elem"]):
            if 1 == 1:  # TODO if elem_type is class
                if diag_type == "unknown":
                    diag_type = "Class"

                elem_id: str = diag_elem.attrib[EA_ATTR["diag_elem_id"]]
                elem_ids.append(elem_id)

        uml_elems: list[ClassDiagramElement] = [
            elem[0] for elem in elems if elem[1] in elem_ids
        ]

        if diag_type == "Class":
            cls_diag: ClassDiagram = ClassDiagram("placeholder")
            cls_diag.elements = uml_elems
            return cls_diag
        else:
            return UMLDiagram("placeholder")

    def try_build_class(self, elem: ET.Element) -> bool:
        self.curr_elem = None

        # Placeholder - just to see if the parser works
        if 1 == 1:  # TODO if elem_type is class
            self.curr_elem = ClassDiagramClass("placeholder")
            return True

        return False

    def try_build_relationship(self, elem: ET.Element) -> bool:
        self.curr_elem = None
        return False
