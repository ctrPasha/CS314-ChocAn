"""
This service provides an interface to add, remove, and update providers and members. 
"""
from dataclasses import asdict
from typing import Optional
from pydantic import BaseModel, Field, ValidationError
from shared_models import PersonData
from peewee import IntegrityError

from data_center.shared_models import PersonSchema, MemberStatus, IdNumberType
from database.members.members_model import Members
from database.connection import db

class MemberSchema(PersonSchema):
    """
    Pydantic schema for a ChocAn member.
    """
    member_id: Optional[IdNumberType] = None
    status: MemberStatus


class ProviderSchema(PersonSchema):
    """
    Pydantic schema for a ChocAn provider.
    """
    provider_id: Optional[IdNumberType] = None


def add_member(status: str, person: PersonData) -> None:
    try:
        new_member = MemberSchema(status=status, **asdict(person))  # validation

        with db:
            Members.create(**new_member.model_dump())

    except ValidationError as e:
        raise ValueError("Violated pydantic model") from e
        # TODO better exception handling

    except IntegrityError as e:
        raise ValueError("Violated database model") from e
        # TODO better exception handling


def update_member(member_id: str, status: str, person: PersonData) -> None:
    try:
        new_member = MemberSchema(status=status, **asdict(person))  # validation
        member_id_int = int(member_id)

        with db:
            member_to_update = Members.get_by_id(member_id)

