from model.base_classes import UMLModel


class ConsitencyFailure():
    pass


class ConsistencyChecker():
    def __init__(self) -> None:
        pass

    def check_model(self, model: UMLModel) -> list[ConsitencyFailure]:
        pass
