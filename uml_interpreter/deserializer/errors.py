from enum import Enum, auto


class ErrorType(Enum):
    ROOT_ERROR = (auto(),)
    MODEL_ERROR = (auto(),)
    EXT_ERROR = (auto(),)
    DIAGS_ERROR = (auto(),)
    DIAG_PROPTY_ERROR = (auto(),)
    MIXED_ELEMS = (auto(),)
    MODEL_ID_MISSING = (auto(),)
    REL_ENDS = (auto(),)
    ATTR_TYPE = (auto(),)
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


class IdMismatchException(InvalidXMLError):
    """
    Exception thrown when no matching ID found in the XML source file.
    """
