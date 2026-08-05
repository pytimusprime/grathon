"""
Input validation helpers for user input
"""

import re
from typing import Any


class InputValidator:
    """Validate common types of user input"""

    @staticmethod
    def is_number(text: str) -> bool:
        """
        Check if text is a number

        Args:
            text: Text to check

        Returns:
            True if text is a valid number

        Examples:
            >>> InputValidator.is_number("123")
            True
            >>> InputValidator.is_number("12.5")
            True
            >>> InputValidator.is_number("abc")
            False
        """
        try:
            float(text)
            return True
        except (ValueError, TypeError):
            return False

    @staticmethod
    def is_integer(text: str) -> bool:
        """
        Check if text is an integer

        Args:
            text: Text to check

        Returns:
            True if text is a valid integer
        """
        try:
            int(text)
            return True
        except (ValueError, TypeError):
            return False

    @staticmethod
    def is_email(text: str) -> bool:
        """
        Check if text is a valid email address

        Args:
            text: Email to validate

        Returns:
            True if text is a valid email format
        """
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return re.match(pattern, text) is not None

    @staticmethod
    def is_url(text: str) -> bool:
        """
        Check if text is a URL

        Args:
            text: URL to validate

        Returns:
            True if text starts with http:// or https://
        """
        pattern = r"^https?://"
        return re.match(pattern, text) is not None

    @staticmethod
    def is_phone(text: str) -> bool:
        """
        Check if text is a phone number

        Accepts formats like:
        - 09123456789
        - +989123456789
        - +98 912 345 6789
        - (912) 345-6789

        Args:
            text: Phone number to validate

        Returns:
            True if text matches phone pattern
        """
        pattern = r"^\+?[0-9\-\(\)\s]{10,}$"
        return re.match(pattern, text) is not None

    @staticmethod
    def is_username(text: str) -> bool:
        """
        Check if text is a valid username (Telegram style)

        Username must:
        - Start with letter or underscore
        - Contain only letters, numbers, underscores
        - Be 3-32 characters

        Args:
            text: Username to validate

        Returns:
            True if text is a valid username
        """
        pattern = r"^[a-zA-Z_][a-zA-Z0-9_]{2,31}$"
        return re.match(pattern, text) is not None

    @staticmethod
    def is_persian(text: str) -> bool:
        """
        Check if text contains Persian/Farsi characters

        Args:
            text: Text to check

        Returns:
            True if text contains Persian characters
        """
        pattern = r"[\u0600-\u06FF]"
        return re.search(pattern, text) is not None

    @staticmethod
    def min_length(text: str, length: int) -> bool:
        """
        Check if text length is at least 'length'

        Args:
            text: Text to check
            length: Minimum required length

        Returns:
            True if text.length >= length
        """
        return len(text) >= length

    @staticmethod
    def max_length(text: str, length: int) -> bool:
        """
        Check if text length is at most 'length'

        Args:
            text: Text to check
            length: Maximum allowed length

        Returns:
            True if text.length <= length
        """
        return len(text) <= length

    @staticmethod
    def length_between(text: str, min_length: int, max_length: int) -> bool:
        """
        Check if text length is between min and max

        Args:
            text: Text to check
            min_length: Minimum length
            max_length: Maximum length

        Returns:
            True if min_length <= text.length <= max_length
        """
        return min_length <= len(text) <= max_length

    @staticmethod
    def matches_pattern(text: str, pattern: str) -> bool:
        """
        Check if text matches a regex pattern

        Args:
            text: Text to check
            pattern: Regex pattern

        Returns:
            True if text matches pattern
        """
        try:
            return re.match(pattern, text) is not None
        except re.error:
            return False

    @staticmethod
    def not_empty(text: str | Any) -> bool:
        """
        Check if text is not empty (after stripping whitespace)

        Args:
            text: Text to check

        Returns:
            True if text is not empty
        """
        if isinstance(text, str):
            return len(text.strip()) > 0
        return bool(text)

    @staticmethod
    def is_command(text: str) -> bool:
        """
        Check if text is a bot command (starts with /)

        Args:
            text: Text to check

        Returns:
            True if text starts with /
        """
        return text.startswith("/") if text else False

    @staticmethod
    def get_command(text: str) -> str | None:
        """
        Extract command name from text

        Args:
            text: Text that might contain command

        Returns:
            Command name without /, or None if not a command

        Examples:
            >>> InputValidator.get_command("/start arg1 arg2")
            "start"
            >>> InputValidator.get_command("normal text")
            None
        """
        if not InputValidator.is_command(text):
            return None

        parts = text.split()
        if not parts:
            return None

        cmd = parts[0][1:]  # Remove leading /
        return cmd if cmd else None

    @staticmethod
    def get_command_args(text: str) -> list[str]:
        """
        Extract command arguments from text

        Args:
            text: Text that might contain command with args

        Returns:
            List of arguments (empty if no args or not a command)

        Examples:
            >>> InputValidator.get_command_args("/start arg1 arg2")
            ["arg1", "arg2"]
            >>> InputValidator.get_command_args("/start")
            []
        """
        if not InputValidator.is_command(text):
            return []

        parts = text.split()
        return parts[1:] if len(parts) > 1 else []
