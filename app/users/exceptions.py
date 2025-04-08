"""
Custom exception classes for user-related errors.

This module provides application-specific exceptions to be used when
user-related operations encounter specific failure conditions. These
exceptions extend from the app-wide base exception classes and provide
clear, domain-relevant error messages.
"""

from app.exceptions import NotFound


class UserNotFound(NotFound):
    """
    Exception raised when a user record cannot be found in the database.

    This exception should be raised in service or DAO layers when a lookup
    for a user by ID or email fails. It inherits from the NotFound base
    exception to standardize error responses across the application.

    Attributes:
        detail (str): A human-readable error message.
    """

    def __init__(self) -> None:
        """
        Initializes the UserNotFound exception with a descriptive message.
        """
        super().__init__("User Not Found!")
