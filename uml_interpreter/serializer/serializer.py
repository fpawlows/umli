from model.model import UMLModel


class Serializer:
    def __init__(self) -> None:
        pass

    def save_to_file(self, path: str) -> UMLModel:
        raise Exception


class XMLSerializer(Serializer):
    pass


class EnterpriseArchitectXMLSerializer(XMLSerializer):
    pass
