from abc import ABC, abstractmethod
from xml import etree as ET


class Source(ABC):
    @abstractmethod
    def read_tree(self):
        pass


class XMLSource(Source):
    @abstractmethod
    def read_tree(self) -> ET.ElementTree:
        pass
