"""
This service provides an interface to add, remove, and update providers and members. 
"""
from dataclasses import asdict
from peewee import PeeweeException

from controllers import member_controllers, providers_controller
import dataclasses as dc
from exceptions import (
    ProviderNotFound,
    MemberNotFound,
    FieldValueError,
    DatabaseError
)

#-------------------------------#
# Get/Add/Update/Remove Members #
#-------------------------------#

def get_members() -> list[dict]:
    raise NotImplementedError("Not implemented yet!")


def add_member(status: str, person: dc.PersonData) -> None:
    """
    Add a new member to the ChocAn database.
    Args:
        status: New member's status. Must be either "A" for active or "I" for inactive.
        person: A PersonData object with the member's personal information.
    Raises:
        pydantic.ValidationError: If a field has an invalid value. Use the .errors() method to get
            a list of structured error dicts.
        ValueError: If the database has already reached the maximum ID number or a field violates
            a database constraint.
    """
    try:
        member_controllers.add_member(status=status, **asdict(person))

    except ValueError as e:
        # TODO remove, since will be changed to specific exceptions
        raise FieldValueError("Invalid field value") from e

    except PeeweeException as e:
        raise DatabaseError("Database transaction failed") from e


def update_member(member_id: str, status: str, person: dc.PersonData) -> None:
    """
    Update the existing member with the ID `member_id` using the field values in `person`.
    Args:
        member_id: The member ID of the member to update.
        status: The member's new status. Must be either "A" for active or "I" for inactive.
        person: A PersonData object with the member's personal information.
    Raises:
        pydantic.ValidationError: If a field has an invalid value. Use the .errors() method to get
            a list of structured error dicts.
        ValueError: If a member with that ID doesn't exist
    """
    try:
        member_controllers.update_member(member_id=member_id, status=status, **asdict(person))

    except ValueError as e:
        # TODO remove, since will be changed to specific exceptions
        raise FieldValueError("Invalid field value") from e

    except PeeweeException as e:
        raise DatabaseError("Database transaction failed") from e


def remove_member(member_id: str) -> None:
    try:
        member_controllers.delete_member(member_id)

    except ValueError as e:
        # TODO remove, since will be changed to MemberNotFound exception
        raise MemberNotFound from e

    except PeeweeException as e:
        raise DatabaseError("Database transaction failed") from e
    

#---------------------------------#
# Get Add/Update/Remove Providers #
#---------------------------------#
def get_providers() -> list[dict]:
    raise NotImplementedError("Not implemented yet!")


def add_provider(person: dc.PersonData) -> None:
    """
    Add a new provider to the database.
    """
    try:
        providers_controller.add_provider(**asdict(person))

    except ValueError as e:
        # TODO remove, since will be changed to specific exceptions
        raise FieldValueError("Invalid field value") from e

    except PeeweeException as e:
        raise DatabaseError("Database transaction failed") from e


def update_provider(provider_id: str, person: dc.PersonData) -> None:
    """
    Update the existing provider with ID `provider_id` using the field values in `person`.
    """
    try:
        providers_controller.update_provider(provider_id=provider_id, **asdict(person))

    except ValueError as e:
        raise ValueError("No member with that ID exists.")
        
    except PeeweeException as e:
        raise DatabaseError("Database transaction failed") from e
        # TODO better exception handling


def remove_provider(provider_id: str) -> None:
    try:
        providers_controller.delete_provider(provider_id)

    except ValueError as e:
        # TODO remove, since will be changed to ProviderNotFound exception
        raise ProviderNotFound from e

    except PeeweeException as e:
        raise DatabaseError("Database transaction failed") from e