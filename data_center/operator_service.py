"""
This service provides an interface to add, remove, and update providers and members. 
"""
from dataclasses import asdict
from typing import Optional
import pydantic
import peewee

from data_center import shared_models
from database.members.members_model import Members
from database.providers.providers_model import Providers
from database.connection import db

class MemberSchema(shared_models.PersonSchema):
    """
    Pydantic schema for a ChocAn member.
    """
    member_id: Optional[shared_models.IdNumberType] = None
    status: shared_models.MemberStatus


class ProviderSchema(shared_models.PersonSchema):
    """
    Pydantic schema for a ChocAn provider.
    """
    provider_id: Optional[shared_models.IdNumberType] = None


#-------------------------------#
# Get/Add/Update/Remove Members #
#-------------------------------#

def get_members() -> list[dict]:
    with db.atomic():
        members = list(Members.select().dicts())
        
    return members


def add_member(status: str, person: shared_models.PersonData) -> None:
    try:
        new_member = MemberSchema(status=status, **asdict(person))  # validation

        with db.atomic():
            Members.create(**new_member.model_dump())

    except pydantic.ValidationError as e:
        raise ValueError("Violated pydantic model") from e
        # TODO better exception handling

    except peewee.IntegrityError as e:
        raise ValueError("Violated database model") from e
        # TODO better exception handling


def update_member(member_id: str, status: str, person: shared_models.PersonData) -> None:
    """
    Update the existing member with ID `provider_id` using the field values in `person`.
    """
    try:
        new_member = MemberSchema(status=status, **asdict(person))  # validation

        with db.atomic():
            member_to_update = Members.get_by_id(member_id)
            member_to_update.update(**new_member.model_dump())

    except pydantic.ValidationError as e:
        raise ValueError("Violated pydantic model") from e
        # TODO better exception handling

    except peewee.DoesNotExist as e:
        raise ValueError("No member with that ID exists.")
        # TODO better exception handling
        
    except peewee.IntegrityError as e:
        raise ValueError("Violated database model.") from e
        # TODO better exception handling


#---------------------------------#
# Get Add/Update/Remove Providers #
#---------------------------------#
def get_providers() -> list[dict]:
    with db.atomic():
        providers = list(Providers.select().dicts())
        
    return providers


def add_provider(person: shared_models.PersonData) -> None:
    """
    Add a new provider to the database.
    """
    try:
        new_provider = MemberSchema(**asdict(person))  # validation

        with db.atomic():
            Providers.create(**new_provider.model_dump())

    except pydantic.ValidationError as e:
        raise ValueError("Violated pydantic model") from e
        # TODO better exception handling

    except peewee.IntegrityError as e:
        raise ValueError("Violated database model") from e
        # TODO better exception handling


def update_provider(provider_id: str, person: shared_models.PersonData) -> None:
    """
    Update the existing provider with ID `provider_id` using the field values in `person`.
    """
    try:
        new_provider = ProviderSchema(provider_id=provider_id, **asdict(person))

        with db.atomic():
            provider_to_update = Members.get_by_id(provider_id)
            provider_to_update.update(**new_provider.model_dump())

    except pydantic.ValidationError as e:
        raise ValueError("Violated pydantic model") from e
        # TODO better exception handling

    except peewee.DoesNotExist as e:
        raise ValueError("No member with that ID exists.")
        # TODO better exception handling
        
    except peewee.IntegrityError as e:
        raise ValueError("Violated database model.") from e
        # TODO better exception handling