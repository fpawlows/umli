import pytest

from uml_interpreter.model.model import UMLModel


@pytest.fixture
def uml_model() -> UMLModel:
    return UMLModel()
