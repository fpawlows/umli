from abc import ABC, abstractmethod
import xml.etree.ElementTree as ET


class Source(ABC):
    @abstractmethod
    def read_tree(self):
        pass


class XMLSource(Source):
    @abstractmethod
    def read_tree(self) -> ET.ElementTree:
        pass
