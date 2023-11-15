import xml.etree.ElementTree as ET


class Source:
    def __init__(self) -> None:
        pass

    def read(self) -> ET.ElementTree:  # type: ignore
        pass


class XMLSource(Source):
    def __init__(self, path: str) -> None:
        super().__init__()
        self.path = path

    def read(self) -> ET.ElementTree:
        return ET.parse(self.path)


class StringSource(Source):
    def __init__(self, xmlstring: str) -> None:
        self.xmlstring = xmlstring
        super().__init__()

    def read(self) -> ET.ElementTree:
        return ET.ElementTree(ET.fromstring(self.xmlstring))
