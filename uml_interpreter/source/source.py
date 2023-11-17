import xml.etree.ElementTree as ET


class XMLSource:
    def __init__(self) -> None:
        pass

    def read_tree(self) -> ET.ElementTree:  # type: ignore
        pass


class FileSource(XMLSource):
    def __init__(self, path: str) -> None:
        super().__init__()
        self.path = path

    def read_tree(self) -> ET.ElementTree:
        return ET.parse(self.path)


class StringSource(XMLSource):
    def __init__(self, xmlstring: str) -> None:
        super().__init__()
        self.xmlstring = xmlstring

    def read_tree(self) -> ET.ElementTree:
        return ET.ElementTree(ET.fromstring(self.xmlstring))
