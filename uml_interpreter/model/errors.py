class ModelParsingError(Exception):
    """
    Exception thrown by Deseralizer, caused by incompatibility of the data with designed model .

    Error message structure:
        Model Setup Error: {error_message}
    """

    def __init__(self, msg: str) -> None:
        """
        Arguments:
            msg {str} -- error message
        """
        self.msg = msg

    def __str__(self):
        return f"Model Setup Error: {self.msg}"


class InvalidModelInitialization(ModelParsingError):
    """
    Exception thrown when tried to collect data for model member object, but couldn't due to an incompatibility.
    """
