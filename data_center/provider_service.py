"""
This service provides an interface for validating provider IDs, member validation and lookup,
and submitting billing records for services. It can also retrieve and return the provider 
directory.
"""
from peewee import PeeweeException

from controllers import member_controllers, providers_controller
from exceptions import DatabaseError, MemberNotFound


def validate_member(member_id: str) -> bool:
    """
    Checks the status of the given member_id.
    Parameters:
        member_id: Member ID string. Doesn't raise an error if it's not a 9-digit string, just returns False.
    Returns:
        True if the member's status is "A" (active) and false otherwise.
    Raises:
        MemberNotFound: If no member with this ID exists.
        DatabaseError: If the database transaction fails or if the member has an incorrect staus string.
    """
    try:
        result = member_controllers.validate_member(member_id)

    except MemberNotFound as e:
        # TODO remove when MemberNotFound added to controller function
        raise
    except ValueError as e:
        # Member status is not a valid string
        raise DatabaseError from e
    except PeeweeException as e:
        raise DatabaseError("Database transaction failed") from e

    return result
