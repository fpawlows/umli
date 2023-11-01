from model.base_classes import UMLModel


class Deserializer:
    def __init__(self) -> None:
        pass

    def read_from_file(path: str) -> UMLModel:
        pass


class XMLDeserializer(Deserializer):
    pass


class EnterpriseArchitectXMLDeserializer(XMLDeserializer):
    pass
