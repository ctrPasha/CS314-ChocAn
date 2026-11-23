"""
This module provides package-wide exceptions that are more descriptive for the kinds of
errors that can occur.
"""

class FieldValueError(Exception):
    """Raised when a value violates a field constraint, wrapping pydantic error details."""
    def __init__(self, message: str, field: str):
        super().__init__(message)
        self.field = field


class MemberNotFound(Exception):
    """Raised when trying to retrieve a member ID that doesn't exist."""
    def __init__(self, id):
        self.member_id = id
        self.message = f"Member with the ID {id} does not exist."
        super.__init__(self.message)


class ProviderNotFound(Exception):
    """Raised when trying to retrieve a provider ID that doesn't exist."""
    def __init__(self, id):
        self.provider_id
        self.message = f"Provider with the ID {id} does not exist."
        super.__init__(self.message)


class DatabaseError(Exception):
    """Wrapper for all kinds of database connection or operation errors"""
    pass