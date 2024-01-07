from __future__ import annotations
import pytest
from typing import Iterable

from uml_interpreter.model.diagrams.class_diagram import (
    ClassRelationship,
    RelationshipType,
    ClassDiagramElement,
    ClassDiagramClass,
)


@pytest.fixture
def class_factory() -> type[ClassFactory]:
    class ClassFactory:
        @staticmethod
        def make_class(*args, **kwargs) -> ClassDiagramClass:
            return ClassDiagramClass(*args, **kwargs)

    return ClassFactory


def test_when_create_default_class_then_initialized(class_factory) -> None:
    # GIVEN
    TEST_CLASS_NAME = "Test Class"

    # WHEN
    test_class: ClassDiagramClass = class_factory.make_class(TEST_CLASS_NAME)

    # THEN
    assert test_class.name == TEST_CLASS_NAME
    assert isinstance(test_class.relations_to, Iterable) and not test_class.relations_to
    assert (
        isinstance(test_class.relations_from, Iterable)
        and not test_class.relations_from
    )


def test_when_add_relation_to_class_then_target_relations_from_updated(
    class_factory,
) -> None:
    # GIVEN
    TEST_SOURCE_CLASS_NAME = "Test Source Class"
    TEST_TARGET_CLASS_NAME = "Test Target Class"
    test_source_class: ClassDiagramClass = class_factory.make_class(
        TEST_SOURCE_CLASS_NAME
    )
    test_target_class: ClassDiagramClass = class_factory.make_class(
        TEST_TARGET_CLASS_NAME
    )

    # WHEN
    test_source_class.add_relationship_to(test_target_class)

    # THEN
    assert len(test_source_class.relations_to) == 1
    is_target_in_source_relations = bool(
        test_target_class
        in map(lambda relation: relation.target, test_source_class.relations_to)
    )
    assert is_target_in_source_relations

    assert len(test_target_class.relations_from) == 1
    is_source_in_target_relations = bool(
        test_source_class
        in map(lambda relation: relation.source, test_target_class.relations_from)
    )
    assert is_source_in_target_relations
