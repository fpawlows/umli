from __future__ import annotations
import pytest
import uuid
from hypothesis import given
from hypothesis.strategies import uuids

from uml_interpreter.model.abstract import UMLObject


@pytest.fixture(scope="module")
def uml_object_factory() -> type[UmlObjectFactory]:
    class UmlObjectFactory:
        @staticmethod
        def make_class(*args, **kwargs) -> UMLObject:
            return UMLObject(*args, **kwargs)

    return UmlObjectFactory


@given(id=uuids())
def test_when_initialized_with_id_then_correct_id_set(uml_object_factory, id: uuid.UUID):
    # GIVEN
    uuid_like_id = str(id)

    # WHEN
    obj = UMLObject(uuid_like_id)

    # THEN
    assert obj.id == uuid_like_id


@given(new_id=uuids())
def test_when_id_set_then_id_changes_accordingly(uml_object_factory, new_id: uuid.UUID):
    # GIVEN
    obj = UMLObject()
    new_uuid_like_id = str(new_id)

    # WHEN
    obj.id = new_uuid_like_id

    # THEN
    assert obj.id == new_uuid_like_id
