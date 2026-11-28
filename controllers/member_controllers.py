from database.members.members_model import Members
import exceptions as exc

def generate_member_id() -> str:
    """
    Generate a unique 9-digit member ID.
    """
    last_member = Members.select().order_by(Members.member_id.desc()).first()
    
    if last_member is None:
        return "000000001"
    
    next_id = int(last_member.member_id) + 1
    
    if next_id > 999999999:
        raise ValueError("Member ID limit reached. Cannot generate a new member ID.")
    
    return f"{next_id:09d}"


def get_member_by_id(member_id: str) -> Members | None:
    """
    Retrieve a member from the database based on the member_id entered.
    If the member exists, return the member object (row) else return None.
    """
    
    return Members.get_or_none(
        (Members.member_id == member_id) & (Members.is_deleted == False)
    )

def update_member_status(member_id: str, new_status: str) -> None:
	"""
	Update the status of a member in the database.
	
	Saves the update if the member exists and the new status is valid ('A' or 'I').
	Raises value error if the member does not exist or if the new status is invalid.
	"""
 
	if new_status not in ['A', 'I', 'S']:
		raise exc.FieldValueError("Invalid status. Must be 'A' (Active), 'I' (Inactive), or 'S' (Suspended).", "status")

 
	member = get_member_by_id(member_id)
	
	if member is None:
		raise exc.MemberNotFound(f"Member with ID {member_id} does not exist.", member_id)
 
	member.status = new_status
	member.save()
 
def validate_member(member_id: str) -> bool:
    
	"""
	determines if a member is valid based on their status in the database.
	Returns True if the member is valid (status 'A'), False if invalid (status 'I'), 
    and raises ValueError if the member does not exist.
	"""
 
	member = get_member_by_id(member_id)
	
	if member is None:
		raise exc.MemberNotFound(f"Member with ID {member_id} does not exist.", member_id)

	if member.status not in ['A', 'I', 'S']:
		raise exc.FieldValueError(f"Member with ID {member_id} has an invalid status: {member.status}", "status")
 
	return member.status == 'A'

def add_member(name: str, street_address: str, city: str, state: str, zip_code: str, status: str) -> Members:
	"""
	Add a new member to the database. and return the new member object.
	Raises ValueError for invalid input or if the ID limit is reached.
	"""

	if not 1 <= len(name) <= 50:
		raise exc.FieldValueError("Name must be between 1 and 50 characters long.", "name")

	if not 5 <= len(street_address) <= 100:
		raise exc.FieldValueError("Street address must be between 5 and 100 characters long.", "street_address")

	if not 1 <= len(city) <= 25:
		raise exc.FieldValueError("City must be between 1 and 25 characters long.", "city")

	if len(state) != 2:
		raise exc.FieldValueError("State must be a 2-character abbreviation.", "state")

	if len(zip_code) != 5 or not zip_code.isdigit():
		raise exc.FieldValueError("Zip code must be a 5-digit number.", "zip_code")

	if status not in ['A', 'I', 'S']:
		raise exc.FieldValueError("Invalid status. Must be 'A' (Active), 'I' (Inactive), or 'S' (Suspended).", "status")

	# Use a transaction to group ID generation and member creation
	# into one database operation, rolling back on failure.
	# SO if it were to fail, the transaction will be rolled back automatically, and no partial data will be saved.
	with Members._meta.database.atomic():
		member_id = generate_member_id()
 
		return Members.create(
			member_id = member_id,
			name = name,
			street_address = street_address,
			city = city,
			state = state,
			zip_code = zip_code,
			status = status,
			is_deleted = False
		)
 
def update_member(member_id: str, name: str, street_address: str, city: str, state: str, zip_code: str) -> None:
	"""
	Update an existing member in the database.
	Raises FieldValueError if any of the provided values are invalid.
	Raises MemberNotFound if the member does not exist.
	"""
	if len(member_id) != 9 or not member_id.isdigit():
		raise exc.FieldValueError("Member ID must be a 9-digit number.", "member_id")

	member = get_member_by_id(member_id)

	if member is None:
		raise exc.MemberNotFound(f"Member with ID {member_id} does not exist.", member_id)

	if not 1 <= len(name) <= 50:
		raise exc.FieldValueError("Name must be between 1 and 50 characters long.", "name")

	if not 5 <= len(street_address) <= 100:
		raise exc.FieldValueError("Street address must be between 5 and 100 characters long.", "street_address")

	if not 1 <= len(city) <= 25:
		raise exc.FieldValueError("City must be between 1 and 25 characters long.", "city")

	if len(state) != 2:
		raise exc.FieldValueError("State must be a 2-character abbreviation.", "state")

	if len(zip_code) != 5 or not zip_code.isdigit():
		raise exc.FieldValueError("Zip code must be a 5-digit number.", "zip_code")

	member.name = name
	member.street_address = street_address
	member.city = city
	member.state = state
	member.zip_code = zip_code
	member.save()
 
def delete_member(member_id: str) -> None:
	"""
	Delete a member from the database.
	Raises MemberNotFound if the member does not exist.
	"""
	member = get_member_by_id(member_id)

	if member is None:
		raise exc.MemberNotFound(f"Member with ID {member_id} does not exist.", member_id)

	member.is_deleted = True
	member.save()