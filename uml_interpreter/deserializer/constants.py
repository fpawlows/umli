DESERIALIZER_CONSTANTS = {
    "UML2_1": "{http://schema.omg.org/spec/UML/2.1}",
    "XMI2_1": "{http://schema.omg.org/spec/XMI/2.1}",
}

EA_TAGS = {
    "ext": f"{DESERIALIZER_CONSTANTS["XMI2_1"]}Extension",
    "model": f"{DESERIALIZER_CONSTANTS["UML2_1"]}Model",
    "elem": "packagedElement",
    "end": "ownedEnd",
    "end_type": "type",
    "diags": "diagrams",
    "diag": "diagram",
    "diag_model": "model",
    "diag_propty": "properties",
    "diag_elems": "elements",
    "diag_elem": "element",

}

EA_ATTR = {
    "elem_id": f"{DESERIALIZER_CONSTANTS["XMI2_1"]}id",
    "elem_type": f"{DESERIALIZER_CONSTANTS["XMI2_1"]}type",
    "elem_name": "name",
    "end_id": f"{DESERIALIZER_CONSTANTS["XMI2_1"]}id",
    "end_type": f"{DESERIALIZER_CONSTANTS["XMI2_1"]}type",
    "end_type_src": f"{DESERIALIZER_CONSTANTS["XMI2_1"]}idref",
    "end_type_dst": f"{DESERIALIZER_CONSTANTS["XMI2_1"]}idref",
    "diag_id": f"{DESERIALIZER_CONSTANTS["XMI2_1"]}id",
    "diag_model_pkg": "package",
    "diag_propty_name": "name",
    "diag_elem_id": "subject",
}


EA_TAGS_EXT = {
    "ext": f"{DESERIALIZER_CONSTANTS["XMI2_1"]}Extension",
    "elems": "elements",
    "elem": "element",
    "elem_model": "model",
    "elem_pkg_propty": "packageproperties",     # if present => elem is a package
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

EA_ATTR_EXT = {
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

UML_TYPES = {
    "pkg": "uml:Pakage",
    "cls": "uml:Class",
    "association": "uml:Association"
}
