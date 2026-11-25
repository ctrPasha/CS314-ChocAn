"""
This service provides an interface to add, remove, and update providers and members. 
"""
from dataclasses import asdict
from peewee import PeeweeException, IntegrityError

from controllers import member_controllers, providers_controller
import provider_service
import chocan_dataclasses as dc
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


def check_member_exists(member_id: str) -> bool:
    """
    Checks database for member with `member_id`.
    Parameters:
        member_id: Member ID string. Doesn't raise an error if it's not a 9-digit string, just returns False.
    Returns:
        True if a member with this ID exists and False otherwise.
    Raises:
        DatabaseError: If the database transaction fails.
    """
    try:
        result = member_controllers.get_member_by_id(member_id)
    except PeeweeException as ex:
        raise DatabaseError("Database transaction failed") from ex

    return (result is not None)


def add_member(status: str, person: dc.PersonData) -> None:
    """
    Add a new member to the ChocAn database.
    Args:
        status: New member's status. Must be either "A" for active or "I" for inactive.
        person: A PersonData object with the member's personal information.
    Raises:
        FieldValueError: If a field has an invalid value.
        DatabaseError: If the database transaction failed or the maximum ID number has already been reached.
    """
    try:
        member_controllers.add_member(status=status, **asdict(person))

    except ValueError as e:
        # TODO remove, since will be changed to specific exceptions
        raise FieldValueError from e
    except IntegrityError as e:
        raise FieldValueError("Violated database constraint") from e
    except PeeweeException as e:
        raise DatabaseError("Database transaction failed") from e


def update_member(member_id: str, person: dc.PersonData) -> None:
    """
    Update the existing member with the ID `member_id` using the field values in `person`.
    Does not include member status. To update member status, use `update_member_status` method.
    Args:
        member_id: The member ID of the member to update.
        person: A PersonData object with the member's personal information.
    Raises:
        FieldValueError: If a field has an invalid value.
        MemberNotFound: If a member with that ID doesn't exist.
        DatabaseError: If the database transaction fails.
    """
    try:
        member_controllers.update_member(member_id, **asdict(person))

    except ValueError as e:
        # TODO remove, since will be changed to MemberNotFound and FieldValueError
        raise FieldValueError from e
    except IntegrityError as e:
        raise FieldValueError("Violated database constraint") from e
    except PeeweeException as e:
        raise DatabaseError("Database transaction failed") from e


def update_member_status(member_id: str, new_status: str) -> None:
    """
    Update an existing member's status to `new_status`.
    Parameters:
        member_id: 9-digit member ID string. The member with this ID will be updated.
        new_status: One character status string, either "A" or "I".
    Raises:
        FieldValueError: If a field has an invalid value.
        MemberNotFound: If a member with that ID doesn't exist.
        DatabaseError: If the database transaction fails.
    """
    try:
        member_controllers.update_member_status(member_id, new_status)

    except ValueError as e:
        # TODO remove, since will be changed FieldValueError or MemberNotFound in controller function
        raise FieldValueError from e 
    except IntegrityError as e:
        raise FieldValueError("Violated database constraint") from e
    except PeeweeException as e:
        raise DatabaseError("Database transaction failed") from e
    

def remove_member(member_id: str) -> None:
    """
    Remove an existing member.
    Parameters:
        member_id: 9-digit member ID string of the member to be deleted.
    Raises:
        MemberNotFound: If a member with that ID doesn't exist.
        DatabaseError: If the database transaction fails.
    """
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

def check_provider_exists(provider_id: str) -> bool:
    """
    Checks database for provider with `provider_id`.
    Parameters:
        provider_id: Provider ID string. Doesn't raise an error if it's not a 9-digit string, just returns False.
    Returns:
        True if a provider with this ID exists and False otherwise.
    Raises:
        DatabaseError: If the database transaction fails.
    """
    try:
        result = providers_controller.get_provider_by_id(provider_id)
    except PeeweeException as ex:
        raise DatabaseError("Database transaction failed") from ex

    return (result is not None)


def add_provider(person: dc.PersonData) -> None:
    """
    Add a new provider to the ChocAn database.
    Args:
        person: A PersonData object with the provider's personal information.
    Raises:
        FieldValueError: If a field has an invalid value.
        DatabaseError: If the database transaction failed or the maximum ID number has already been reached.
    """
    try:
        providers_controller.add_provider(**asdict(person))

    except ValueError as e:
        # TODO remove, since will be changed to FieldValueError
        raise FieldValueError from e
    except IntegrityError as e:
        raise FieldValueError("Violated database constraint") from e
    except PeeweeException as e:
        raise DatabaseError("Database transaction failed") from e


def update_provider(provider_id: str, person: dc.PersonData) -> None:
    """
    Update the existing provider with the ID `provider_id` using the field values in `person`.
    Args:
        provider_id: The provider ID of the member to update.
        person: A PersonData object with the provider's personal information.
    Raises:
        FieldValueError: If a field has an invalid value.
        ProviderNotFound: If a provider with that ID doesn't exist.
        DatabaseError: If the database transaction fails.
    """
    try:
        providers_controller.update_provider(provider_id, **asdict(person))

    except ValueError as e:
        # TODO remove, since will be changed to ProviderNotFound and FieldValueError
        raise FieldValueError from e
    except IntegrityError as e:
        raise FieldValueError("Violated database constraint") from e
    except PeeweeException as e:
        raise DatabaseError("Database transaction failed") from e


def remove_provider(provider_id: str) -> None:
    """
    Remove an existing provider.
    Parameters:
        provider_id: 9-digit provider ID string of the provider to be deleted.
    Raises:
        ProviderNotFound: If a provider with that ID doesn't exist.
        DatabaseError: If the database transaction fails.
    """
    try:
        providers_controller.delete_provider(provider_id)

    except ValueError as e:
        # TODO remove, since will be changed to ProviderNotFound exception
        raise ProviderNotFound from e

    except PeeweeException as e:
        raise DatabaseError("Database transaction failed") from e
