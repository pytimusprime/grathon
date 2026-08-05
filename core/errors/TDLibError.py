"""TDLib API error response exception"""


class TDLibError(Exception):
    """Raised when TDLib API returns an error response

    Attributes:
        code: TDLib error code
        message: Error message from TDLib
    """

    def __init__(self, code: int, message: str):
        """Initialize TDLibError

        Args:
            code: Error code from TDLib
            message: Error message from TDLib
        """
        self.code = code
        self.message = message
        super().__init__(f"TDLib error {code}: {message}")
