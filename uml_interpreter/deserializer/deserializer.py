"""
UML Model deserializer module

The module includes the following:
- InvalidXMLError
- Deserializer
- XMLDeserializer
- EnterpriseArchitectXMLDeserializer
"""

import xml.etree.ElementTree as ET
from abc import ABC, abstractmethod
from typing import Any

from uml_interpreter.deserializer.constants import (
    CLASS_IFACE_MAPPING,
    CLASS_REL_MAPPING_TYPE,
    CLASS_RELATIONSHIPS,
    EA_ATTR,
    EA_ATTR_MAPPING,
    EA_TAGS,
    ERROR_MESS,
    TAGS_ERRORS,
    ErrorType,
)
from uml_interpreter.model.base_classes import UMLDiagram, UMLModel
from uml_interpreter.model.class_diagram import (
    ClassDiagram,
    ClassDiagramAttribute,
    ClassDiagramElement,
    ClassDiagramMethod,
    ClassDiagramMethodParameter,
    ClassRelationship,
)
from uml_interpreter.source.source import FileSource, XMLSource


class InvalidXMLError(Exception):
    """
    Exception thrown by Deseralizer, caused by invalid XML structure.

    Error message structure:
        Parser Error: {error_message}
    """

    def __init__(self, msg: str) -> None:
        """
        Arguments:
            msg {str} -- error message
        """
        self.msg = msg

    def __str__(self):
        return f"Parser Error: {self.msg}"


class Deserializer(ABC):
    def __init__(self, source: XMLSource) -> None:
        self._source: XMLSource = source

    @abstractmethod
    def read_model(self) -> UMLModel:
        pass

    @property
    @abstractmethod
    def source(self):
        pass

    @source.setter
    @abstractmethod
    def source(self, source):
        pass


class XMLDeserializer(Deserializer):
    def __init__(self, source: XMLSource) -> None:
        super().__init__(source)

    def read_model(self) -> UMLModel:
        try:
            tree: ET.ElementTree = self.source.read_tree()
            return self.parse_model(tree)
        except ET.ParseError as exc:
            raise InvalidXMLError(exc.msg)

    @abstractmethod
    def parse_model(self, tree: ET.ElementTree) -> UMLModel:
        pass

    @property
    def source(self) -> XMLSource:
        return self._source

    @source.setter
    def source(self, source: XMLSource) -> None:
        self._source = source


class EnterpriseArchitectXMLDeserializer(XMLDeserializer):
    def __init__(self, source: XMLSource) -> None:
        super().__init__(source)
        self.temp_rel_ids = []

    def parse_model(self, tree: ET.ElementTree) -> UMLModel:
        root = self.get_root(tree)

        model_node = self.get_node(root, "model")

        elems: list[
            tuple[ClassDiagramElement | ClassRelationship | Any, str]
        ] = self.parse_elems(
            model_node
        )  # TODO Any -> Other diagram type elements

        self.assign_ends(
            [rel[0] for rel in elems if isinstance(rel[0], ClassRelationship)],
            [elem for elem in elems if isinstance(elem[0], ClassDiagramElement)],
        )

        diagrams: list[UMLDiagram] = self.parse_diagrams(
            root, [elem for elem in elems if isinstance(elem[0], ClassDiagramElement)]
        )

        return UMLModel(
            diagrams=diagrams,
            filename=self.source.path if isinstance(self.source, FileSource) else None,
        )

    def get_root(self, tree: ET.ElementTree) -> ET.Element:
        root = tree.getroot()
        if not isinstance(root, ET.Element):
            raise InvalidXMLError(ERROR_MESS[ErrorType.ROOT_ERROR])
        return root

    def get_node(self, root: ET.Element, tag: str) -> ET.Element:
        node = root.find(EA_TAGS[tag])
        if node is None:
            raise InvalidXMLError(TAGS_ERRORS[tag])
        return node

    def parse_elems(
        self, model: ET.Element
    ) -> list[tuple[ClassDiagramElement | Any, str]]:
        elems_info: list[tuple[ClassDiagramElement | ClassRelationship | Any, str]] = []

        for elem in model.iter(EA_TAGS["elem"]):
            elem_info = self.parse_elem(elem)
            if elem_info:
                elems_info.append(elem_info)

        return elems_info

    def parse_elem(
        self, elem: ET.Element
    ) -> tuple[ClassDiagramElement | ClassRelationship | Any, str] | None:
        if self.skip_package(elem):
            return None
        if self.try_build_class_or_iface(elem) or self.try_build_relationship(elem):
            if not (elem_id := elem.attrib.get(EA_ATTR["elem_id"])):
                raise InvalidXMLError(ERROR_MESS[ErrorType.MODEL_ID_MISSING])
            return (self.curr_elem, elem_id)

    def assign_ends(
        self,
        rels: list[ClassRelationship],
        elems: list[tuple[ClassDiagramElement, str]],
    ):
        for rel in rels:
            for rel_ids in self.temp_rel_ids:
                if rel == rel_ids[0]:
                    rel.source = next(
                        (elem for elem, elem_id in elems if elem_id == rel_ids[1][0]),
                        None,
                    )
                    if isinstance(rel.source, ClassDiagramElement):
                        rel.source.relations_from.append(rel)
                    rel.target = next(
                        (elem for elem, elem_id in elems if elem_id == rel_ids[1][1]),
                        None,
                    )
                    if isinstance(rel.target, ClassDiagramElement):
                        rel.target.relations_to.append(rel)
        self.temp_rel_ids = []

    def parse_diagrams(
        self,
        root: ET.Element,
        elems: list[tuple[ClassDiagramElement | Any, str]],
    ) -> list[UMLDiagram]:
        diagrams: list[UMLDiagram] = []

        ext = self.get_node(root, "ext")
        diags = self.get_node(ext, "diags")

        self.populate_diagrams(elems, diagrams, diags)

        return diagrams

    def populate_diagrams(
        self,
        elems: list[tuple[ClassDiagramElement | Any, str]],
        diagrams: list[UMLDiagram],
        diags: ET.Element,
    ) -> None:
        for diag in diags.iter(EA_TAGS["diag"]):
            diagrams.append(self.get_filled_diag(diag, elems))

    def get_filled_diag(
        self, diag: ET.Element, elems: list[tuple[ClassDiagramElement | Any, str]]
    ) -> UMLDiagram:
        diag_name = self.get_node(diag, "diag_propty").attrib[
            EA_ATTR["diag_propty_name"]
        ]
        diag_elems = diag.find(EA_TAGS["diag_elems"])
        if diag_elems is None:
            return UMLDiagram(diag_name)

        elem_ids: list[str] = []
        for diag_elem in diag_elems.iter(EA_TAGS["diag_elem"]):
            elem_ids.append(diag_elem.attrib[EA_ATTR["diag_elem_id"]])

        uml_elems: list[ClassDiagramElement | Any] = [
            elem[0] for elem in elems if elem[1] in elem_ids
        ]

        if all(isinstance(elem, ClassDiagramElement) for elem in uml_elems):
            return ClassDiagram(diag_name, uml_elems)
        else:
            raise InvalidXMLError(ERROR_MESS[ErrorType.MIXED_ELEMS])

    def skip_package(self, elem: ET.Element) -> bool:
        if elem.attrib[EA_ATTR["elem_type"]] == "uml:Package":
            return True
        return False

    def try_build_class_or_iface(self, elem: ET.Element) -> bool:
        if ElemClass := CLASS_IFACE_MAPPING.get(elem.attrib[EA_ATTR["elem_type"]]):
            self.curr_elem = ElemClass(elem.attrib[EA_ATTR["elem_name"]])

            attrs: list[ClassDiagramAttribute] = self.build_attributes(elem)
            meths: list[ClassDiagramMethod] = self.build_methods(elem)
            self.curr_elem.attributes = attrs
            self.curr_elem.methods = meths
            return True
        return False

    def build_attributes(self, elem: ET.Element) -> list[ClassDiagramAttribute]:
        attrs: list[ClassDiagramAttribute] = []
        for attr in elem.iter(EA_TAGS["elem_attr"]):
            name: str = attr.attrib[EA_ATTR["elem_attr_name"]]
            if not (
                type := EA_ATTR_MAPPING.get(
                    self.get_node(attr, "elem_attr_type").attrib[
                        EA_ATTR["elem_attr_type"]
                    ]
                )
            ):
                type = ""
            attrs.append(ClassDiagramAttribute(name, type))
        return attrs

    def build_methods(self, elem: ET.Element) -> list[ClassDiagramMethod]:
        meths: list[ClassDiagramMethod] = []
        for meth in elem.iter(EA_TAGS["elem_meth"]):
            name: str = meth.attrib[EA_ATTR["elem_meth_name"]]
            ret_type: str | None = ""
            params: list[ClassDiagramMethodParameter] = []
            for param in meth.iter(EA_TAGS["elem_meth_param"]):
                if (
                    param_name := param.attrib[EA_ATTR["elem_meth_param_name"]]
                ) == "return":
                    if not (
                        ret_type := EA_ATTR_MAPPING.get(
                            param.attrib[EA_ATTR["elem_meth_ret_type"]]
                        )
                    ):
                        ret_type = ""

                else:
                    if not (
                        type := EA_ATTR_MAPPING.get(
                            self.get_node(param, "elem_meth_param_type").attrib[
                                EA_ATTR["elem_meth_param_type"]
                            ]
                        )
                    ):
                        type = ""

                    params.append(ClassDiagramMethodParameter(param_name, type))

            meths.append(ClassDiagramMethod(name, ret_type, params))
        return meths

    def try_build_relationship(self, elem: ET.Element) -> bool:
        if not (rel_name := elem.attrib.get(EA_ATTR["end_name"])):
            rel_name = ""

        if elem.attrib[EA_ATTR["elem_type"]] in CLASS_RELATIONSHIPS:
            end_ids: list[str] = ["", ""]
            end_roles: list[str | None] = ["", ""]
            end_minmax: list[tuple[str, str]] = [("", ""), ("", "")]
            for end in elem.iter(EA_TAGS["end"]):
                if "EAID_dst" in end.attrib[EA_ATTR["end_id"]]:
                    end_ids[1] = self.get_node(end, "end_type").attrib[
                        EA_ATTR["end_type_dst"]
                    ]
                    low = ""
                    high = ""
                    for src_vals in end.findall(EA_TAGS["end_low"]):
                        dst_low = src_vals.attrib[EA_ATTR["end_low_type"]]
                        if dst_low == "uml:LiteralUnlimitedNatural":
                            low = "inf"
                        else:
                            low = src_vals.attrib[EA_ATTR["end_low_val"]]

                    for src_vals in end.findall(EA_TAGS["end_high"]):
                        dst_high = src_vals.attrib[EA_ATTR["end_high_type"]]
                        if dst_high == "uml:LiteralUnlimitedNatural":
                            high = "inf"
                        else:
                            high = src_vals.attrib[EA_ATTR["end_high_val"]]

                    end_minmax[1] = (low, high)
                    end_roles[1] = end.attrib.get(EA_ATTR["end_name_src"])

                elif "EAID_src" in end.attrib[EA_ATTR["end_id"]]:
                    end_ids[0] = self.get_node(end, "end_type").attrib[
                        EA_ATTR["end_type_src"]
                    ]

                    low = ""
                    high = ""
                    for src_vals in end.findall(EA_TAGS["end_low"]):
                        src_low = src_vals.attrib[EA_ATTR["end_low_type"]]
                        if src_low == "uml:LiteralUnlimitedNatural":
                            low = "inf"
                        else:
                            low = src_vals.attrib[EA_ATTR["end_low_val"]]

                    for src_vals in end.findall(EA_TAGS["end_high"]):
                        src_high = src_vals.attrib[EA_ATTR["end_high_type"]]
                        if src_high == "uml:LiteralUnlimitedNatural":
                            high = "inf"
                        else:
                            high = src_vals.attrib[EA_ATTR["end_high_val"]]

                    end_minmax[0] = (low, high)
                    end_roles[0] = end.attrib.get(EA_ATTR["end_name_src"])

            if not (
                all(isinstance(end, str) for end in end_ids)
                and all(end != "" for end in end_ids)
            ):
                raise InvalidXMLError(ERROR_MESS[ErrorType.REL_ENDS])

            type = CLASS_REL_MAPPING_TYPE[elem.attrib[EA_ATTR["elem_type"]]]
            self.curr_elem = ClassRelationship(
                type, rel_name, end_roles[0], end_roles[1], end_minmax[0], end_minmax[1]
            )
            self.temp_rel_ids.append((self.curr_elem, end_ids))
            return True
        return False
