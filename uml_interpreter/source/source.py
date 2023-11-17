import xml.etree.ElementTree as ET
from abc import ABC, abstractmethod


class Source(ABC):
    @abstractmethod
    def read_tree(self):
        pass


class XMLSource(Source):
    @abstractmethod
    def read_tree(self) -> ET.ElementTree:
        pass


class FileSource(XMLSource):
    def __init__(self, path: str) -> None:
        self.path = path

    def read_tree(self) -> ET.ElementTree:
        return ET.parse(self.path)


class StringSource(XMLSource):
    def __init__(self, xmlstring: str) -> None:
        self.xmlstring = xmlstring

    def read_tree(self) -> ET.ElementTree:
        return ET.ElementTree(ET.fromstring(self.xmlstring))
