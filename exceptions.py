"""
This module provides package-wide exceptions that are more descriptive for the kinds of
errors that can occur.
"""

class FieldValueError(Exception):
    """Raised when a value violates a field constraint"""
    def __init__(self, message: str, field: str):
        self.message = message
        self.field = field
        super().__init__(message)


class MemberNotFound(Exception):
    """Raised when trying to retrieve a member ID that doesn't exist."""
    def __init__(self, message: str, id: str = None):
        self.member_id = id
        self.message = message
        # self.message = f"Member with the ID {id} does not exist."
        super().__init__(self.message)


class ProviderNotFound(Exception):
    """Raised when trying to retrieve a provider ID that doesn't exist."""
    def __init__(self, message:str, id: str = None):
        self.provider_id = id
        self.message = message
        # self.message = f"Provider with the ID {id} does not exist."
        super().__init__(self.message)


class DatabaseError(Exception):
    """Wrapper for all kinds of database connection or operation errors"""
    pass