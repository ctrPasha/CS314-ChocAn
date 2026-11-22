from peewee import BooleanField, Check, CharField
from database.base_model import BaseModel


class Members(BaseModel):
    member_id = CharField(
        primary_key = True,
        max_length = 9,
        constraints = [
            Check("length(member_id) = 9"),
            Check("member_id NOT GLOB '*[^0-9]*'"),
        ],
    )
    name = CharField(
        max_length = 50,
        constraints = [
            Check("length(name) BETWEEN 1 AND 50")
        ]
    )
    street_address = CharField(
        max_length = 100, constraints = [Check("length(street_address) BETWEEN 5 AND 100")]
    )
    city = CharField(
        max_length = 25, constraints = [Check("length(city) BETWEEN 1 AND 25")]
    )

    state = CharField(max_length = 2, constraints = [Check("length(state) = 2")])
    zip_code = CharField(
        max_length = 5,
        constraints = [
            Check("length(zip_code) = 5"),
            Check("zip_code NOT GLOB '*[^0-9]*'"),
        ],
    )
    
    status = CharField(max_length = 1, constraints = [Check("status IN ('A', 'I')")])
    
    is_deleted = BooleanField(default = False, constraints = [Check("is_deleted IN (0, 1)")])

    class Meta:
        table_name = "Members"
