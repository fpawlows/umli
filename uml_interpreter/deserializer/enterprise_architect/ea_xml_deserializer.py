from typing import Any, Optional, Callable
from functools import wraps
from collections import defaultdict, deque
import logging

import xml.etree.ElementTree as ET

from uml_interpreter.deserializer.enterprise_architect.constants import (
    CLASS_IFACE_MAPPING,
    CLASS_REL_MAPPING_TYPE,
    CLASS_RELATIONSHIPS_TYPES,
    EA_ATTR,
    EA_ATTR_MAPPING,
    EA_TAGS,
)
from uml_interpreter.deserializer.abstract import XMLDeserializer
from uml_interpreter.deserializer.enterprise_architect.utils import (
    SourceDestinationPair,
    SetRelationshipSource,
    SetRelationshipTarget,
)
from uml_interpreter.deserializer.errors import (
    ERROR_MESS,
    TAGS_ERRORS,
    ErrorType,
    InvalidXMLError,
    IdMismatchException,
)
from uml_interpreter.model.diagrams.abstract import UMLDiagram
from uml_interpreter.model.abstract import UMLObject
from uml_interpreter.model.model import UMLModel
from uml_interpreter.model.diagrams.class_diagram import (
    ClassDiagram,
    ClassDiagramAttribute,
    ClassDiagramElement,
    ClassDiagramMethod,
    ClassDiagramMethodParameter,
    ClassRelationship,
)
from uml_interpreter.source.source import FileSource, StringSource, XMLSource


def evaluate_elements_afterwards(blocking: bool = False) -> Callable:
    """
    Decorator that evaluates all elements from the evaluation queue.
    :arg blocking - if set to True, it raises IdMismatchException when ID present as a key in evaluation
        queue is not present in the ID to instance mapping.
    """

    def wrapper(func: Callable) -> Callable:
        @wraps(func)
        def inner(self, *args, **kwargs) -> Any:
            """
            Function used for decoration of class methods, therefore self is expected to always be the first argument.
            """
            returned_value = func(self, *args, **kwargs)
            self._evaluate_elements(blocking)
            return returned_value

        return inner

    return wrapper


class EAXMLDeserializer(XMLDeserializer):
    IGNORED_XML_ELEMENTS = ["uml:Package"]
    """
    Classes ignored during parsing.
    """

    def __init__(self, source: XMLSource) -> None:
        self._source: XMLSource = source
        self._id_to_instance_mapping: dict[str, UMLObject] = dict()
        self._id_to_evaluation_queue: dict[str, deque[Callable]] = defaultdict(deque)
        """
        Queue of functions to be called when Instance of the Object with given ID is available.
        The Instance has to be given as an argument to function call.
        """

    def _evaluate_elements(self, blocking: bool = False) -> None:
        """
        Function that evaluates all elements from the evaluation queue.
        :arg blocking - if set to True, it raises IdMismatchException when ID present as key in the evaluation
            queue is not present in the ID to instance mapping. Used for partial evaluation.
        """
        for element_id, evaluation_queue in self._id_to_evaluation_queue.items():
            try:
                element_instance = self._id_to_instance_mapping[element_id]
            except KeyError as ex:
                message = f"Couldn't associate given referred object id: {element_id} with any known instance."
                if blocking:
                    raise IdMismatchException(message) from ex
                else:
                    logging.log(logging.INFO, message)
                    continue

            while evaluation_queue:
                function_to_call = evaluation_queue.popleft()
                function_to_call(element_instance)

    @classmethod
    def from_string(cls, string):
        return cls(StringSource(string))

    @classmethod
    def from_path(cls, path):
        return cls(FileSource(path))

    def _parse_model(self, tree: ET.ElementTree) -> UMLModel:
        root = self._get_root(tree)

        model_node = self._get_mandatory_node(root, "model")

        elems: list[UMLObject] = self._parse_elems(model_node)

        diagrams: list[UMLDiagram] = self._parse_diagrams(
            root, [elem for elem in elems if isinstance(elem, ClassDiagramElement)]
        )

        return UMLModel(
            diagrams=diagrams,
            filename=self.source.path if isinstance(self.source, FileSource) else None,
        )

    def _get_root(self, tree: ET.ElementTree) -> ET.Element:
        root = tree.getroot()
        if not isinstance(root, ET.Element):
            raise InvalidXMLError(ERROR_MESS[ErrorType.ROOT_ERROR])
        return root

    def _get_mandatory_node(self, root: ET.Element, tag: str) -> ET.Element:
        """
        Retrieves the node of XML document containing specified tag.
        Its absence raises InvalidXMLError.
        """
        if (node := self._get_node_by_tag(root, tag)) is None:
            raise InvalidXMLError(TAGS_ERRORS[tag])
        return node

    def _get_node_by_tag(self, root: ET.Element, tag: str) -> Optional[ET.Element]:
        return root.find(EA_TAGS[tag])

    def _parse_elem(self, elem: ET.Element) -> Optional[UMLObject]:
        if not self._is_supported_element(elem):
            return None

        if elem_id := elem.attrib.get(EA_ATTR["elem_id"]):
            if parsed_elem := self._try_build_class_or_iface(elem):
                parsed_elem.id = elem_id
                self._id_to_instance_mapping[elem_id] = parsed_elem

            elif parsed_elem := self._try_build_relationship(elem):
                parsed_elem.id = elem_id
                self._id_to_instance_mapping[elem_id] = parsed_elem

            else:
                logging.log(
                    logging.INFO,
                    """Retrieved object is unknown - couldn't build class or
                    interface or their relationship based on the object data.""",
                )
                return None

            return parsed_elem

        else:
            raise InvalidXMLError(ERROR_MESS[ErrorType.MODEL_ID_MISSING])

    @evaluate_elements_afterwards()
    def _parse_elems(self, model_node: ET.Element) -> list[UMLObject]:
        """
        Functions dependent on the initialization of the element with id given as the key of the dictionary.
        """
        elements_info = [
            element_info
            for element in model_node.iter(EA_TAGS["elem"])
            if (element_info := self._parse_elem(element)) is not None
        ]
        return elements_info

    def _parse_diagrams(
        self,
        root: ET.Element,
        elems: list[UMLObject],
    ) -> list[UMLDiagram]:
        diagrams: list[UMLDiagram] = []

        ext = self._get_mandatory_node(root, "ext")
        diags = self._get_mandatory_node(ext, "diags")

        self._populate_diagrams(elems, diagrams, diags)

        return diagrams

    def _populate_diagrams(
        self,
        elems: list[UMLObject],
        diagrams: list[UMLDiagram],
        diags: ET.Element,
    ) -> None:
        for diag in diags.iter(EA_TAGS["diag"]):
            diagrams.append(self._get_filled_diag(diag, elems))

    def _get_filled_diag(self, diag: ET.Element, elems: list[UMLObject]) -> UMLDiagram:
        diag_name = self._get_mandatory_node(diag, "diag_propty").attrib.get(
            EA_ATTR["diag_propty_name"]
        )

        if not (diag_elems := diag.find(EA_TAGS["diag_elems"])):
            return UMLDiagram(diag_name)

        elem_ids: list[str] = [
            diag_elem.attrib[EA_ATTR["diag_elem_id"]]
            for diag_elem in diag_elems.iter(EA_TAGS["diag_elem"])
        ]

        uml_elems: list[UMLObject] = [elem for elem in elems if elem.id in elem_ids]

        if all(isinstance(elem, ClassDiagramElement) for elem in uml_elems):
            return ClassDiagram(diag_name, uml_elems)
        else:
            raise InvalidXMLError(ERROR_MESS[ErrorType.MIXED_ELEMS])

    def _is_supported_element(self, elem: ET.Element) -> bool:
        is_supported_element = (
            elem.attrib[EA_ATTR["elem_type"]] not in self.IGNORED_XML_ELEMENTS
        )
        return is_supported_element

    def _try_build_class_or_iface(
        self, elem: ET.Element
    ) -> Optional[ClassDiagramElement]:
        if ElemClass := CLASS_IFACE_MAPPING.get(elem.attrib[EA_ATTR["elem_type"]]):
            curr_elem = ElemClass(elem.attrib[EA_ATTR["elem_name"]])

            attrs: list[ClassDiagramAttribute] = self._build_attributes(elem)
            meths: list[ClassDiagramMethod] = self._build_methods(elem)

            curr_elem.attributes = attrs
            curr_elem.methods = meths
            return curr_elem

        return None

    def _build_attributes(self, elem: ET.Element) -> list[ClassDiagramAttribute]:
        attrs: list[ClassDiagramAttribute] = []
        for attr in elem.iter(EA_TAGS["elem_attr"]):
            name: str = attr.attrib[EA_ATTR["elem_attr_name"]]
            if not (
                type_name := EA_ATTR_MAPPING.get(
                    self._get_mandatory_node(attr, "elem_attr_type").attrib[
                        EA_ATTR["elem_attr_type"]
                    ]
                )
            ):
                type_name = ""
            attrs.append(ClassDiagramAttribute(name, type_name))
        return attrs

    def _build_methods(self, elem: ET.Element) -> list[ClassDiagramMethod]:
        meths: list[ClassDiagramMethod] = []
        for meth in elem.iter(EA_TAGS["elem_meth"]):
            if (name := meth.attrib.get(EA_ATTR["elem_meth_name"])) is None:
                name = ""

            ret_type: Optional[str] = ""
            params: list[ClassDiagramMethodParameter] = []
            for param in meth.iter(EA_TAGS["elem_meth_param"]):
                if (
                    param_name := param.attrib.get(EA_ATTR["elem_meth_param_name"])
                ) == "return":
                    if not (
                        ret_type := EA_ATTR_MAPPING.get(
                            param.attrib[EA_ATTR["elem_meth_ret_type"]]
                        )
                    ):
                        ret_type = ""

                else:
                    if not (
                        type_name := EA_ATTR_MAPPING.get(
                            self._get_mandatory_node(
                                param, "elem_meth_param_type"
                            ).attrib[EA_ATTR["elem_meth_param_type"]]
                        )
                    ):
                        type_name = ""

                    params.append(ClassDiagramMethodParameter(param_name, type_name))

            meths.append(ClassDiagramMethod(name, ret_type, params))
        return meths

    def _create_relation_source_side(
        self, end: ET.Element
    ) -> ClassRelationship.RelationshipSide:
        source_side = ClassRelationship.RelationshipSide()

        low = "inf"
        high = "inf"
        for src_vals in end.findall(EA_TAGS["end_low"]):
            src_low = src_vals.attrib[EA_ATTR["end_low_type"]]
            # TODO: use configuration / constants file with types mappings
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

        source_side.min_max_multiplicity = (low, high)

        if role := end.attrib.get(EA_ATTR["end_name_src"]):
            source_side.role = role

        return source_side

    def _create_relation_target_side(
        self, end: ET.Element
    ) -> ClassRelationship.RelationshipSide:
        target_side = ClassRelationship.RelationshipSide()

        low = "inf"
        high = "inf"
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

        target_side.min_max_multiplicity = (low, high)

        if role := end.attrib.get(EA_ATTR["end_name_dst"]):
            target_side.role = role

        return target_side

    def _try_build_relationship(self, elem: ET.Element) -> Optional[ClassRelationship]:
        if elem.attrib[EA_ATTR["elem_type"]] in CLASS_RELATIONSHIPS_TYPES:
            rel_name = elem.attrib.get(EA_ATTR["end_name"])
            type_name = CLASS_REL_MAPPING_TYPE[elem.attrib[EA_ATTR["elem_type"]]]

            # Final relationship uninitialized placeholder
            processed_relation = ClassRelationship(type_name, rel_name)
            ends_ids = SourceDestinationPair()

            for end in elem.iter(EA_TAGS["end"]):
                if end.attrib[EA_ATTR["end_id"]].startswith("EAID_src"):
                    ends_ids.source = self._get_mandatory_node(end, "end_type").attrib[
                        EA_ATTR["end_type_src"]
                    ]
                    processed_relation.source_side = self._create_relation_source_side(
                        end
                    )

                elif end.attrib[EA_ATTR["end_id"]].startswith("EAID_dst"):
                    ends_ids.target = self._get_mandatory_node(end, "end_type").attrib[
                        EA_ATTR["end_type_dst"]
                    ]
                    processed_relation.target_side = self._create_relation_target_side(
                        end
                    )

            if not (all(vars(ends_ids).values())):
                raise InvalidXMLError(ERROR_MESS[ErrorType.REL_ENDS])

            self._id_to_evaluation_queue[ends_ids.source].append(
                SetRelationshipSource(processed_relation)
            )
            self._id_to_evaluation_queue[ends_ids.target].append(
                SetRelationshipTarget(processed_relation)
            )

            return processed_relation
        return None
