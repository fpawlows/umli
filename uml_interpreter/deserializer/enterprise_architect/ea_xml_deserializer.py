from typing import Any, Optional, Callable, Iterable
from functools import wraps
import logging
# TODO: add Logger instance 
from collections import defaultdict, deque
from uml_interpreter.deserializer.enterprise_architect.constants import (
    CLASS_IFACE_MAPPING,
    CLASS_REL_MAPPING_TYPE,
    CLASS_RELATIONSHIPS_TYPES,
    EA_ATTR,
    EA_ATTR_MAPPING,
    EA_TAGS,
)
from uml_interpreter.deserializer.abstract import XMLDeserializer
from uml_interpreter.deserializer.enterprise_architect.utils import ElemWithId, EndMinMax, RelEndRoles, RelEndsMinMax, RelIds, RelWithIds, SetRelationshipSource, SetRelationshipTarget
from uml_interpreter.deserializer.errors import (
    ERROR_MESS,
    TAGS_ERRORS,
    ErrorType,
    InvalidXMLError,
    IdMismatchException
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
from uml_interpreter.source.source import FileSource, StringSource, XMLSource
import xml.etree.ElementTree as ET


class EAXMLDeserializer(XMLDeserializer):
    UNSUPPORTED_XML_ELEMENTS = ["uml:Package"]
    """
    Classes ignored during parsing.
    """

    def __init__(self, source: XMLSource) -> None:
        self._source: XMLSource = source
        self._temp_rel_ids: list[RelWithIds] = []
        self._id_to_instance_mapping: dict[str, ET.Element] = dict()
        # TODO: consider using proxy or lazy evaluation for this

        self._id_to_evaluation_queue: dict[str, Iterable[Callable]] = defaultdict(deque)
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
                    logging.log('INFO', message)
                    continue
                
            while evaluation_queue:
                function_to_call = evaluation_queue.popleft()
                function_to_call(element_instance)


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

    @classmethod
    def from_string(cls, string):
        return cls(StringSource(string))

    @classmethod
    def from_path(cls, path):
        return cls(FileSource(path))

    def _parse_model(self, tree: ET.ElementTree) -> UMLModel:
        root = self._get_root(tree)

        model_node = self._get_mandatory_node(root, 'model')

        elems: list[ElemWithId] = self._parse_elems(model_node)

        self._assign_ends(
            [rel.elem for rel in elems if isinstance(rel.elem, ClassRelationship)],
            [elem for elem in elems if isinstance(elem.elem, ClassDiagramElement)],
        )

        diagrams: list[UMLDiagram] = self._parse_diagrams(
            root, [elem for elem in elems if isinstance(elem.elem, ClassDiagramElement)]
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
        if (node := self._get_node_by_tag(self, root, tag)) is None:
            raise InvalidXMLError(TAGS_ERRORS[tag])
        return node

    def _get_node_by_tag(self, root: ET.Element, tag: str) -> ET.Element:
        return root.find(EA_TAGS[tag])

    # def _parse_elems(self, model_node: ET.Element) -> list[ElemWithId]:
    #     elements_info: list[ElemWithId] = [
    #         element_info
    #         for element in
    #         model_node.iter(EA_TAGS["elem"])
    #         if (element_info := self._parse_elem(element))
    #     ]

    #     return elements_info

    # def _parse_elem(self, elem: ET.Element) -> Optional[ElemWithId]:
    #     if not self._is_supported_element(elem):
    #         return None
    #     if self._try_build_class_or_iface(elem) or self._try_build_relationship(elem):
    #         if not (elem_id := elem.attrib.get(EA_ATTR["elem_id"])):
    #             raise InvalidXMLError(ERROR_MESS[ErrorType.MODEL_ID_MISSING])
    #         return ElemWithId(self._curr_elem, elem_id)

    def _parse_elem(self, elem: ET.Element) -> Optional[ElemWithId]:
        if not self._is_supported_element(elem):
            return None

        if (elem_id := elem.attrib.get(EA_ATTR["elem_id"])):

            if parsed_elem := self._try_build_class_or_iface(elem):
                self._id_to_instance_mapping[elem_id] = parsed_elem
                # TODO: rethink return value

            elif parsed_elem := self._try_build_relationship(elem):
                self._id_to_instance_mapping[elem_id] = parsed_elem

            else:
                raise InvalidXMLError(ERROR_MESS[ErrorType.MODEL_ID_MISSING])

        return ElemWithId(self._curr_elem, elem_id)

    @evaluate_elements_afterwards()
    def _parse_elems(self, model_node: ET.Element) -> list[ElemWithId]:
        """
        Functions dependent on the initialization of the element with id given as the key of the dictionary.
        """
        elements_info = [self._parse_elem(element) for element in model_node.iter(EA_TAGS["elem"])]
        return elements_info


        # def _assign_ends(
    #     self,
    #     rels: list[ClassRelationship],
    #     elems: list[ElemWithId],
    # ):
    #     for rel in rels:
    #         for rel_ids in self._temp_rel_ids:
    #             if rel == rel_ids.rel:
    #                 rel.source = next(
    #                     (
    #                         elem
    #                         for elem, elem_id in elems
    #                         if elem_id == rel_ids.ids.src_id
    #                     ),
    #                     None,
    #                 )
    #                 if isinstance(rel.source, ClassDiagramElement):
    #                     rel.source.relations_from.append(rel)
    #
    #                 rel.target = next(
    #                     (
    #                         elem
    #                         for elem, elem_id in elems
    #                         if elem_id == rel_ids.ids.dst_id
    #                     ),
    #                     None,
    #                 )
    #                 if isinstance(rel.target, ClassDiagramElement):
    #                     rel.target.relations_to.append(rel)
    #
    #     self._temp_rel_ids = []

    def _parse_diagrams(
        self,
        root: ET.Element,
        elems: list[ElemWithId],
    ) -> list[UMLDiagram]:
        diagrams: list[UMLDiagram] = []

        ext = self._get_mandatory_node(root, "ext")
        diags = self._get_mandatory_node(ext, "diags")

        self._populate_diagrams(elems, diagrams, diags)

        return diagrams

    def _populate_diagrams(
        self,
        elems: list[ElemWithId],
        diagrams: list[UMLDiagram],
        diags: ET.Element,
    ) -> None:
        for diag in diags.iter(EA_TAGS["diag"]):
            diagrams.append(self._get_filled_diag(diag, elems))

    def _get_filled_diag(self, diag: ET.Element, elems: list[ElemWithId]) -> UMLDiagram:
        diag_name = self._get_mandatory_node(diag, "diag_propty").attrib.get(
            EA_ATTR["diag_propty_name"]
        )

        if not (diag_elems := diag.find(EA_TAGS["diag_elems"])):
            return UMLDiagram(diag_name)

        elem_ids: list[str] = []
        for diag_elem in diag_elems.iter(EA_TAGS["diag_elem"]):
            elem_ids.append(diag_elem.attrib[EA_ATTR["diag_elem_id"]])

        uml_elems: list[ClassDiagramElement | Any] = [
            elem.elem for elem in elems if elem.id in elem_ids
        ]

        if all(isinstance(elem, ClassDiagramElement) for elem in uml_elems):
            return ClassDiagram(diag_name, uml_elems)
        else:
            raise InvalidXMLError(ERROR_MESS[ErrorType.MIXED_ELEMS])


    def _is_supported_element(self, elem: ET.Element) -> bool:
        is_supported_element = (
            elem.attrib[EA_ATTR["elem_type"]]
            not in self.UNSUPPORTED_XML_ELEMENTS
            )
        return is_supported_element

    def _try_build_class_or_iface(self, elem: ET.Element) -> Optional[ClassDiagramElement]:

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
                type := EA_ATTR_MAPPING.get(
                    self._get_mandatory_node(attr, "elem_attr_type").attrib[
                        EA_ATTR["elem_attr_type"]
                    ]
                )
            ):
                type = ""
            attrs.append(ClassDiagramAttribute(name, type))
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
                        type := EA_ATTR_MAPPING.get(
                            self._get_mandatory_node(
                                param, "elem_meth_param_type"
                            ).attrib[EA_ATTR["elem_meth_param_type"]]
                        )
                    ):
                        type = ""

                    params.append(ClassDiagramMethodParameter(param_name, type))

            meths.append(ClassDiagramMethod(name, ret_type, params))
        return meths

    def _try_build_relationship(self, elem: ET.Element) -> Optional[ClassRelationship]:
        if not (rel_name := elem.attrib.get(EA_ATTR["end_name"])):
            # TODO: why "end_name"
            # TODO: change na None
            rel_name = ""

        if elem.attrib[EA_ATTR["elem_type"]] in CLASS_RELATIONSHIPS_TYPES:
            end_ids: RelIds = RelIds("", "")
            end_roles: RelEndRoles = RelEndRoles("", "")
            end_minmax: RelEndsMinMax = RelEndsMinMax(
                EndMinMax("", ""), EndMinMax("", "")
            )

            for end in elem.iter(EA_TAGS["end"]):
                low = ""
                high = ""
                # TODO: can it be starts_with()?
                if "EAID_src" in end.attrib[EA_ATTR["end_id"]]:
                    end_ids.src_id = self._get_mandatory_node(end, "end_type").attrib[
                        EA_ATTR["end_type_src"]
                    ]

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

                    end_minmax.src_minmax = EndMinMax(low, high)

                    if role := end.attrib.get(EA_ATTR["end_name_src"]):
                        end_roles.src_role = role

                elif "EAID_dst" in end.attrib[EA_ATTR["end_id"]]:
                    end_ids.dst_id = self._get_mandatory_node(end, "end_type").attrib[
                        EA_ATTR["end_type_dst"]
                    ]

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

                    end_minmax.dst_minmax = EndMinMax(low, high)

                    if role := end.attrib.get(EA_ATTR["end_name_dst"]):
                        end_roles.dst_role = role

            if not (
                all(isinstance(end, str) for end in vars(end_ids).values())
                and all(end != "" for end in vars(end_ids).values())
            ):
                raise InvalidXMLError(ERROR_MESS[ErrorType.REL_ENDS])

            type = CLASS_REL_MAPPING_TYPE[elem.attrib[EA_ATTR["elem_type"]]]
            curr_elem = ClassRelationship(
                type,
                rel_name,
                end_roles.src_role,
                end_roles.dst_role,
                end_minmax.src_minmax,
                end_minmax.dst_minmax,
            )

            self._id_to_evaluation_queue.update(end_ids.src_id, SetRelationshipSource(curr_elem))
            self._id_to_evaluation_queue.update(end_ids.dst_id, SetRelationshipTarget(curr_elem))
            # self._temp_rel_ids.append(RelWithIds(curr_elem, end_ids))
            return curr_elem
        return None
