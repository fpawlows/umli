from model.base_classes import UMLModel


class Serializer:
    def __init__(self) -> None:
        pass

    def save_to_file(path: str) -> UMLModel:
        pass


class XMLSerializer(Serializer):
    pass


class EnterpriseArchitectXMLSerializer(XMLSerializer):
    pass
