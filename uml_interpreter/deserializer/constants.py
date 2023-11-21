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
    "end_name": "name",
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
