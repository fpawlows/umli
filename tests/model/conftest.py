import pytest

from uml_interpreter.model.abstract import UMLModel


@pytest.fixture
def uml_model() -> UMLModel:
    return UMLModel()
