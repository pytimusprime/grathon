"""
Handle sending message function error
"""


class SendMessageException(Exception):
    """
    SendMessageException
    """

    def __init__(self, error_information: str | None = None,
                 exception: Exception | None = None):
        super().__init__(
            'Sending Message error',
            error_information,
            exception
        )
        self.error_information: str | None = error_information
        self.exception: Exception | None = exception
