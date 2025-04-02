"""
This module defines custom exceptions for the application.

It includes specific exceptions for handling 'Not Found' errors,
such as the NotFound exception class.
"""

from fastapi import HTTPException


class NotFound(HTTPException):
    """
    Custom exception class for handling 'Not Found' errors.

    This class extends the FastAPI HTTPException class to provide
    a specific exception for 404 Not Found errors.

    Attributes:
        detail (str): A detailed error message describing the reason for the exception.
    """

    def __init__(self, detail: str = "Not Found") -> None:
        """
        Initializes the NotFound exception with a 404 status code and a detailed message.

        Args:
            detail (str): A detailed error message describing the reason for the exception.
        """
        super().__init__(404, detail)


class NoContent(HTTPException):
    """
    Custom exception class for handling 'No Content' responses.

    This class extends the FastAPI HTTPException class to provide
    a specific exception for 204 No Content responses.

    Attributes:
        description (str): A detailed message describing the reason for the exception.
    """

    def __init__(self, description: str = "No Content") -> None:
        """
        Initializes the NoContent exception with a 204 status code and a detailed message.

        Args:
            description (str): A detailed message describing the reason for the exception.
        """
        super().__init__(204, description)
