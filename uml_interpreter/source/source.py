import xml.etree.ElementTree as ET
from uml_interpreter.source.abstract import XMLSource


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
