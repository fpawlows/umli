"""
XML Deserializer constants (e.g. tags' and atrributes' names)

The module includes the following:
- DESERIALIZER_CONSTANTS
- EA_TAGS
- EA_ATTR
- EA_TAGS_EXT
- EA_ATTR_EXT
- CLASS_DIAGRAM_TYPES
- CLASS_IFACE_MAPPING
- ERROR_MESS
- TAGS_ERRORS
- ErrorType
"""

from enum import Enum, auto

from uml_interpreter.model.class_diagram import (ClassDiagramClass,
                                                 ClassDiagramElement,
                                                 ClassDiagramInterface)

DESERIALIZER_CONSTANTS: dict[str, str] = {
    "UML2_1": "{http://schema.omg.org/spec/UML/2.1}",
    "XMI2_1": "{http://schema.omg.org/spec/XMI/2.1}",
}
"""
XML namespaces
"""

EA_TAGS: dict[str, str] = {
    "root": f"{DESERIALIZER_CONSTANTS["UML2_1"]}XMI",
    # Model
    "model": f"{DESERIALIZER_CONSTANTS["UML2_1"]}Model",
    "elem": "packagedElement",
    "end": "ownedEnd",
    "end_type": "type",
    "end_low": "lowerValue",
    "end_high": "upperValue",
    "elem_attr": "ownedAttribute",
    "elem_attr_type": "type",
    "elem_meth": "ownedOperation",
    "elem_meth_param": "ownedParameter",
    "elem_meth_param_type": "type",



    # Diagrams
    "ext": f"{DESERIALIZER_CONSTANTS["XMI2_1"]}Extension",
    "diags": "diagrams",
    "diag": "diagram",
    "diag_propty": "properties",
    "diag_elems": "elements",
    "diag_elem": "element",
}
"""
Enterprise Architect XML tags
"""

EA_ATTR: dict[str, str] = {
    # Model
    "elem_id": f"{DESERIALIZER_CONSTANTS["XMI2_1"]}id",
    "elem_type": f"{DESERIALIZER_CONSTANTS["XMI2_1"]}type",
    "elem_name": "name",
    "end_id": f"{DESERIALIZER_CONSTANTS["XMI2_1"]}id",
    "end_type": f"{DESERIALIZER_CONSTANTS["XMI2_1"]}type",
    "end_type_src": f"{DESERIALIZER_CONSTANTS["XMI2_1"]}idref",
    "end_type_dst": f"{DESERIALIZER_CONSTANTS["XMI2_1"]}idref",
    "end_name_src": "name",
    "end_name_dst": "name",
    "end_low_val": "value",
    "end_high_val": "value",
    "end_low_type": f"{DESERIALIZER_CONSTANTS["XMI2_1"]}type",
    "end_high_type": f"{DESERIALIZER_CONSTANTS["XMI2_1"]}type",
    "elem_attr_name": "name",
    "elem_attr_type": "href",
    "elem_meth_name": "name",
    "elem_meth_param_type": "href",
    "elem_meth_param_name": "name",
    "elem_meth_ret_type": "type",

    # Diagrams
    "diag_id": f"{DESERIALIZER_CONSTANTS["XMI2_1"]}id",
    "diag_propty_name": "name",
    "diag_elem_id": "subject",
}
"""
Enterprise Architect XML attributes
"""

EA_ATTR_MAPPING = {
    "http://schema.omg.org/spec/UML/2.1/uml.xml#Integer": "integer",
    "EAnone_void": "void",
}


EA_TAGS_EXT: dict[str, str] = {
    "root": f"{DESERIALIZER_CONSTANTS["UML2_1"]}XMI",
    "ext": f"{DESERIALIZER_CONSTANTS["XMI2_1"]}Extension",
    "elems": "elements",
    "elem": "element",
    "elem_model": "model",
    "elem_pkg_propty": "packageproperties",
    "conns": "connectors",
    "conn": "connector",
    "conn_src": "source",
    "conn_trgt": "target",
    "conn_propty": "properties",
    "diags": "diagrams",
    "diag": "diagram",
    "diag_model": "model",
    "diag_propty": "properties",
    "diag_elems": "elements",
    "diag_elem": "element",
}
"""
Enterprise Architect alternative XML tags
"""

EA_ATTR_EXT: dict[str, str] = {
    "elem_id": f"{DESERIALIZER_CONSTANTS["XMI2_1"]}idref",
    "elem_type": f"{DESERIALIZER_CONSTANTS["XMI2_1"]}type",
    "elem_name": "name",
    "elem_model_pkg": "package",
    "conn_id": f"{DESERIALIZER_CONSTANTS["XMI2_1"]}idref",
    "conn_name": "name",
    "conn_src_id": f"{DESERIALIZER_CONSTANTS["XMI2_1"]}idref",
    "conn_trgt_id": f"{DESERIALIZER_CONSTANTS["XMI2_1"]}idref",
    "conn_propty_type": "ea_type",
    "conn_propty_dir": "direction",
    "diag_id": f"{DESERIALIZER_CONSTANTS["XMI2_1"]}id",
    "diag_model_pkg": "package",
    "diag_propty_name": "name",
    "diag_elem_id": "subject",
}
"""
Enterprise Architect alternative XML attributes
"""

CLASS_RELATIONSHIPS: list[str] = ["uml:Association"]
"""
UML Class Relationships types
"""

CLASS_REL_MAPPING_TYPE: dict[str, str] = {
    "uml:Association": "Association",
}
"""
Mapping of relationship elements to their type name
"""

CLASS_IFACE_MAPPING: dict[str, type[ClassDiagramElement]] = {
    "uml:Class": ClassDiagramClass,
    "uml:Interface": ClassDiagramInterface
}
"""
Mapping of class and interface uml elements to python classes
"""


class ErrorType(Enum):
    ROOT_ERROR = auto(),
    MODEL_ERROR = auto(),
    EXT_ERROR = auto(),
    DIAGS_ERROR = auto(),
    DIAG_PROPTY_ERROR = auto(),
    MIXED_ELEMS = auto(),
    MODEL_ID_MISSING = auto(),
    REL_ENDS = auto(),
    ATTR_TYPE = auto(),
    METH_PARAM_TYPE = auto()


ERROR_MESS: dict[ErrorType, str] = {
    ErrorType.ROOT_ERROR: "No XMI node found in the XML file.",
    ErrorType.MODEL_ERROR: "No Model node found in the XML file.",
    ErrorType.EXT_ERROR: "No Extension node found in the XML file.",
    ErrorType.DIAGS_ERROR: "No diagrams found in the XML file.",
    ErrorType.DIAG_PROPTY_ERROR: "Invalid diagram node in XML file. Missing properties tag.",
    ErrorType.MIXED_ELEMS: "Mixed elements' types for diagram in XML file.",
    ErrorType.MODEL_ID_MISSING: "UML Model element is missing an id!",
    ErrorType.REL_ENDS: "Relationship is missing at least one of the ends!",
    ErrorType.ATTR_TYPE: "Attribute is missing a type!",
    ErrorType.METH_PARAM_TYPE: "Parameter is missing a type!",
}

TAGS_ERRORS: dict[str, str] = {
    "root": ERROR_MESS[ErrorType.ROOT_ERROR],
    "model": ERROR_MESS[ErrorType.MODEL_ERROR],
    "ext": ERROR_MESS[ErrorType.EXT_ERROR],
    "diags": ERROR_MESS[ErrorType.DIAGS_ERROR],
    "diag_propty": ERROR_MESS[ErrorType.DIAG_PROPTY_ERROR],
    "elem_attr_type": ERROR_MESS[ErrorType.ATTR_TYPE],
    "elem_meth_param_type": ERROR_MESS[ErrorType.METH_PARAM_TYPE],
}
"""
Error messages for XML tags
"""
