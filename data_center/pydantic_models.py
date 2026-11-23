from typing import Annotated, Optional
from enum import StrEnum
from pydantic import BaseModel, Field, BeforeValidator

#--------------------------#
# Internal data validation #
#--------------------------#
### ID numbers ###
def strip_leading_zeroes(value: str | int) -> str | int:
    """
    Helper function that strips leading zeroes from a digit string and returns it as an integer.
    """
    if isinstance(value, str):
        value = value.strip()
        if value.isdigit():
            return value.lstrip("0") or 0
    return value

IdNumberType = Annotated[int, BeforeValidator(strip_leading_zeroes), Field(ge=1, le=999999999)]

### Member status enum ###
class MemberStatus(StrEnum):
    """
    Represents a member's current enrollment status in ChocAn. The single letter values are how
    status is represented in the database.
    """
    ACTIVE = "A"
    INACTIVE = "I"


### Schema for person base class ###
class PersonSchema(BaseModel):
    """
    BaseModel that defines the attributes of a person, including their name and an address.
    """
    name: str = Field(max_length=50)
    street_address: str = Field(max_length=100)
    city: str = Field(max_length=25)
    state: str = Field(
        min_length=2,
        max_length=2, 
        pattern=r'^[A-Z]{2}$'
    )
    zip_code: str = Field(
        min_length=5,
        max_length=5,
        pattern=r'^\d*$'
    )


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