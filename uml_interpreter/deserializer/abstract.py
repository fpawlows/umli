import xml.etree.ElementTree as ET
from abc import ABC, abstractmethod
from uml_interpreter.deserializer.errors import InvalidXMLError
from uml_interpreter.model.base_classes import UMLModel
from uml_interpreter.source.source import XMLSource


class Deserializer(ABC):
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
    def read_model(self) -> UMLModel:
        try:
            tree: ET.ElementTree = self.source.read_tree()
            return self._parse_model(tree)
        except ET.ParseError as exc:
            raise InvalidXMLError(exc.msg)

    @property
    def source(self) -> XMLSource:
        return self._source

    @source.setter
    def source(self, source: XMLSource) -> None:
        self._source = source

    @abstractmethod
    def _parse_model(self, tree: ET.ElementTree) -> UMLModel:
        pass
