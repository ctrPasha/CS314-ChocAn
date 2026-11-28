import pytest
from controllers import member_controllers as mc
import exceptions as exc
from database.members.members_model import Members


def test_get_member_by_id_none(test_db):
    member = mc.get_member_by_id("123456789")
    assert member is None


def test_get_member_by_id_existing(test_db):
    
    # Create a test member in the database
    test_member = Members.create(
        member_id="123456789",
        name="Test Member",
        street_address="123 Test St",
        city="Testville",
        state="TS",
        zip_code="12345",
        status="A",
    )
    
    # Retrieve the member using the controller function
    retrieved_member = mc.get_member_by_id("123456789")
    
    # Assert that the retrieved member matches the created member
    assert retrieved_member is not None
    assert retrieved_member.member_id == test_member.member_id
    assert retrieved_member.name == test_member.name
    assert retrieved_member.street_address == test_member.street_address
    assert retrieved_member.city == test_member.city
    assert retrieved_member.state == test_member.state
    assert retrieved_member.zip_code == test_member.zip_code
    assert retrieved_member.status == test_member.status


def test_get_member_by_id_soft_deleted(test_db):
    
    # Create a test member in the database with is_deleted = True
    Members.create(
        member_id="987654321",
        name="Soft Deleted Member",
        street_address="456 Soft Deleted St",
        city="Softville",
        state="SD",
        zip_code="54321",
        status="A",
        is_deleted=True,
    )
    
    # Attempt to retrieve the soft-deleted member
    member = mc.get_member_by_id("987654321")
    
    # Assert that the member is None since it is soft-deleted
    assert member is None


def test_update_member_status_valid(test_db):
    
    # Create a test member in the database
    Members.create(
        member_id="987654321",
        name="Another Test Member",
        street_address="456 Another St",
        city="Anotherville",
        state="AT",
        zip_code="54321",
        status="A",
    )
    
    # Update the member's status to 'I' (Inactive)
    mc.update_member_status("987654321", "I")
    
    # Retrieve the member again to check the updated status
    updated_member = mc.get_member_by_id("987654321")
    assert updated_member is not None
    assert updated_member.status == "I"


def test_update_member_status_invalid_status(test_db):
    
    # Create a test member in the database
    Members.create(
        member_id="111222333",
        name="Invalid Status Test Member",
        street_address="789 Invalid St",
        city="Invalidville",
        state="IV",
        zip_code="67890",
        status="A",
    )
    
    # Verify that an invalid status raises ValueError
    with pytest.raises(exc.FieldValueError) as exc_info:
        mc.update_member_status("111222333", "X")
    assert str(exc_info.value) == (
        "Invalid status. Must be 'A' (Active), 'I' (Inactive), or 'S' (Suspended)."
    )
    
    # Verify that the member's status was not changed
    member = mc.get_member_by_id("111222333")
    assert member is not None
    assert member.status == "A"


def test_update_member_status_nonexistent_member(test_db):
    
    # Verify that updating a non-existent member raises ValueError
    with pytest.raises(exc.MemberNotFound) as exc_info:
        mc.update_member_status("000000000", "A")
        
    assert str(exc_info.value) == "Member with ID 000000000 does not exist."


def test_update_member_status_soft_deleted(test_db):
    Members.create(
        member_id="444555666",
        name="Soft Deleted Member",
        street_address="404 Soft Deleted St",
        city="Softville",
        state="SD",
        zip_code="44444",
        status="A",
        is_deleted=True,
    )
    
    with pytest.raises(exc.MemberNotFound) as exc_info:
        mc.update_member_status("444555666", "I")
    assert str(exc_info.value) == ("Member with ID 444555666 does not exist.")


def test_validate_member_active(test_db):
    
    # Create a test member in the database with status 'A' (Active)
    Members.create(
        member_id="555666777",
        name="Active Member",
        street_address="101 Active St",
        city="Activeville",
        state="AC",
        zip_code="11111",
        status="A",
    )
    
    # Validate the member
    is_valid = mc.validate_member("555666777")
    assert is_valid is True


def test_validate_member_inactive(test_db):
    
    # Create a test member in the database with status 'I' (Inactive)
    Members.create(
        member_id="888999000",
        name="Inactive Member",
        street_address="202 Inactive St",
        city="Inactiveville",
        state="IN",
        zip_code="22222",
        status="I",
    )
    
    # Validate the member
    is_valid = mc.validate_member("888999000")
    assert is_valid is False


def test_validate_member_nonexistent(test_db):
    
    # Verify that validating a non-existent member raises ValueError
    with pytest.raises(exc.MemberNotFound) as exc_info:
        mc.validate_member("000000000")
    assert str(exc_info.value) == "Member with ID 000000000 does not exist."


def test_validate_member_soft_deleted(test_db):
    
    # Create a test member in the database with status 'A' (Active) and is_deleted = True
    Members.create(
        member_id="444555666",
        name="Soft Deleted Member",
        street_address="404 Soft Deleted St",
        city="Softville",
        state="SD",
        zip_code="44444",
        status="A",
        is_deleted=True,
    )
    
    # Verify that validating a soft-deleted member raises ValueError
    with pytest.raises(exc.MemberNotFound) as exc_info:
        mc.validate_member("444555666")
        
    assert str(exc_info.value) == "Member with ID 444555666 does not exist."


def test_add_member_valid(test_db):
    
    # Add a valid member with an automatically generated ID
    created_member = mc.add_member(
        name="New Member",
        street_address="303 New St",
        city="Newville",
        state="NW",
        zip_code="33333",
        status="A",
    )
    
    # Verify that the member was added successfully
    member = mc.get_member_by_id(created_member.member_id)
    assert member is not None
    assert member.member_id == "000000001"
    assert member.street_address == "303 New St"
    assert member.city == "Newville"
    assert member.state == "NW"
    assert member.zip_code == "33333"
    assert member.name == "New Member"
    assert member.status == "A"
    assert member.is_deleted is False


def test_add_member_auto_increment(test_db):
    
    # Add the original member to the database
    first_member = mc.add_member(
        name="Duplicate Member",
        street_address="404 Duplicate St",
        city="Duplicateville",
        state="DP",
        zip_code="44444",
        status="A",
    )
    
    # A second member receives a new ID rather than reusing the first ID
    second_member = mc.add_member(
        name="Second Member",
        street_address="505 Second St",
        city="Secondville",
        state="SC",
        zip_code="55555",
        status="I",
    )
    
    assert first_member.member_id == "000000001"
    assert second_member.member_id == "000000002"
    
    # Verify the original member was not overwritten
    member = mc.get_member_by_id(first_member.member_id)
    assert member is not None
    assert member.name == "Duplicate Member"
    assert member.street_address == "404 Duplicate St"
    assert member.status == "A"
    
    # Verify two different members were created
    assert Members.select().count() == 2

@pytest.mark.parametrize(
    "invalid_name", ["", "A" * 51]  # Empty name  # Name exceeds 50 characters
)
def test_add_member_invalid_name(test_db, invalid_name):
    
    # Verify that adding a member with an invalid name raises ValueError
    with pytest.raises(exc.FieldValueError) as exc_info:
        mc.add_member(
            name=invalid_name,
            street_address="606 Invalid St",
            city="Invalidville",
            state="IV",
            zip_code="66666",
            status="A",
        )
    assert str(exc_info.value) == "Name must be between 1 and 50 characters long."
    
    # Verify no member was added to the database
    assert Members.select().count() == 0

@pytest.mark.parametrize(
    "invalid_street_address",
    [
        "",  # Empty street address
        "A" * 4,  # Street address less than 10 characters
        "A" * 101,  # Street address exceeds 100 characters
    ],
)

def test_add_member_invalid_street_address(test_db, invalid_street_address):
    
    # Verify that an invalid street address raises ValueError
    with pytest.raises(exc.FieldValueError) as exc_info:
        mc.add_member(
            name="Valid Name",
            street_address=invalid_street_address,
            city="Validville",
            state="VV",
            zip_code="66666",
            status="A",
        )
        
    assert str(exc_info.value) == (
        "Street address must be between 5 and 100 characters long."
    )
    
    # Verify no member was added to the database
    assert Members.select().count() == 0

@pytest.mark.parametrize(
    "invalid_city", ["", "A" * 26]  # Empty city  # City exceeds 25 characters
)
def test_add_member_invalid_city(test_db, invalid_city):
    
    # Verify that an invalid city raises ValueError
    with pytest.raises(exc.FieldValueError) as exc_info:
        mc.add_member(
            name="Valid Name",
            street_address="707 Valid St",
            city=invalid_city,
            state="VV",
            zip_code="66666",
            status="A",
        )
    assert str(exc_info.value) == ("City must be between 1 and 25 characters long.")
    
    # Verify no member was added to the database
    assert Members.select().count() == 0


@pytest.mark.parametrize(
    "invalid_state",
    [
        "",  # Empty state
        "A",  # State less than 2 characters
        "AAA",  # State more than 2 characters
    ],
)

def test_add_member_invalid_state(test_db, invalid_state):
    
    # Verify that an invalid state raises ValueError
    with pytest.raises(exc.FieldValueError) as exc_info:
        mc.add_member(
            name="Valid Name",
            street_address="808 Valid St",
            city="Validville",
            state=invalid_state,
            zip_code="66666",
            status="A",
        )
    assert str(exc_info.value) == ("State must be a 2-character abbreviation.")
    
    # Verify no member was added to the database
    assert Members.select().count() == 0

@pytest.mark.parametrize(
    "invalid_zip_code",
    [
        "",  # Empty zip code
        "1234",  # Zip code less than 5 digits
        "123456",  # Zip code more than 5 digits
        "ABCDE",  # Zip code with non-digit characters
        "A1234",  # Zip code with non-digit characters mixed with digits
    ],
)

def test_add_member_invalid_zip_code(test_db, invalid_zip_code):
    
    # Verify that an invalid zip code raises ValueError
    with pytest.raises(exc.FieldValueError) as exc_info:
        mc.add_member(
            name="Valid Name",
            street_address="909 Valid St",
            city="Validville",
            state="VV",
            zip_code=invalid_zip_code,
            status="A",
        )
        
    assert str(exc_info.value) == ("Zip code must be a 5-digit number.")
    
    # Verify no member was added to the database
    assert Members.select().count() == 0


@pytest.mark.parametrize(
    "invalid_status",
    [
        "",  # Empty status
        "X",  # Invalid status character
        "Active",  # Status more than 1 character
    ],
)
def test_add_member_invalid_status(test_db, invalid_status):
    
    # Verify that an invalid status raises ValueError
    with pytest.raises(exc.FieldValueError) as exc_info:
        mc.add_member(
            name="Valid Name",
            street_address="1010 Valid St",
            city="Validville",
            state="VV",
            zip_code="66666",
            status=invalid_status,
        )
        
    assert str(exc_info.value) == (
        "Invalid status. Must be 'A' (Active), 'I' (Inactive), or 'S' (Suspended)."
    )
    
    # Verify no member was added to the database
    assert Members.select().count() == 0


def test_generate_member_id_empty(test_db):
    
    # The first generated member ID should be nine digits
    assert mc.generate_member_id() == "000000001"


def test_generate_member_id_existing(test_db):
    
    # Existing IDs determine the next generated ID
    Members.create(
        member_id="000000025",
        name="Existing Member",
        street_address="1111 Valid St",
        city="Validville",
        state="VV",
        zip_code="66666",
        status="A",
    )
    assert mc.generate_member_id() == "000000026"


def test_generate_member_id_limit(test_db):
    
    # A maximum nine-digit member ID cannot be incremented
    Members.create(
        member_id="999999999",
        name="Last Member",
        street_address="1111 Valid St",
        city="Validville",
        state="VV",
        zip_code="66666",
        status="A",
    )
    with pytest.raises(ValueError) as exc_info:
        mc.generate_member_id()
    assert str(exc_info.value) == (
        "Member ID limit reached. Cannot generate a new member ID."
    )

def test_add_member_soft_delete_no_id_reuse(test_db):
    
    # Add a member
    first_member = mc.add_member(
        name="Valid Name",
        street_address="1111 Valid St",
        city="Validville",
        state="VV",
        zip_code="66666",
        status="A",
    )
    
    # Soft delete the member
    mc.delete_member(first_member.member_id)
    
    # Adding a second member should generate a new ID
    second_member = mc.add_member(
        name="Second Member",
        street_address="2222 Valid St",
        city="Validville",
        state="VV",
        zip_code="66666",
        status="A",
    )
    
    assert first_member.member_id == "000000001"
    assert second_member.member_id == "000000002"
    
    # The deleted member still exists in the database, but is hidden by the controller
    assert mc.get_member_by_id(first_member.member_id) is None
    assert Members.get_by_id(first_member.member_id).is_deleted is True
    assert Members.select().count() == 2


def test_update_member_valid(test_db):
    
    # Add a member to update
    member = mc.add_member(
        name="Valid Name",
        street_address="1111 Valid St",
        city="Validville",
        state="VV",
        zip_code="66666",
        status="A",
    )
    
    # Update the member's information
    mc.update_member(
        member_id=member.member_id,
        name="Updated Name",
        street_address="2222 Updated St",
        city="Updatedville",
        state="UU",
        zip_code="77777",
    )
    
    # Retrieve the updated member
    updated_member = mc.get_member_by_id(member.member_id)
    assert updated_member is not None
    assert updated_member.name == "Updated Name"
    assert updated_member.street_address == "2222 Updated St"
    assert updated_member.city == "Updatedville"
    assert updated_member.state == "UU"
    assert updated_member.zip_code == "77777"
    assert updated_member.status == "A"


def test_update_member_none_existant(test_db):
    
    # Attempt to update a non-existent member
    with pytest.raises(exc.MemberNotFound) as exc_info:
        mc.update_member(
            member_id="000000999",
            name="Non-existent Member",
            street_address="9999 Nowhere St",
            city="Nowhereville",
            state="NN",
            zip_code="99999",
        )
        
    assert str(exc_info.value) == "Member with ID 000000999 does not exist."

def test_update_member_soft_deleted(test_db):
    
    # Add a member and soft delete it
    member = mc.add_member(
        name="Valid Name",
        street_address="1111 Valid St",
        city="Validville",
        state="VV",
        zip_code="66666",
        status="A",
    )
    mc.delete_member(member.member_id)
    
    # Attempt to update the soft-deleted member
    with pytest.raises(exc.MemberNotFound) as exc_info:
        mc.update_member(
            member_id=member.member_id,
            name="Updated Name",
            street_address="2222 Updated St",
            city="Updatedville",
            state="UU",
            zip_code="77777",
        )
    assert str(exc_info.value) == f"Member with ID {member.member_id} does not exist."

@pytest.mark.parametrize("invalid_id", ["", "123", "1234567890", "ABC123456"])
def test_update_member_invalid_id(test_db, invalid_id):
    
    # Attempt to update a member with an invalid ID
    with pytest.raises(exc.FieldValueError) as exc_info:
        mc.update_member(
            member_id=invalid_id,
            name="Invalid ID Member",
            street_address="1234 Invalid St",
            city="Invalidville",
            state="II",
            zip_code="12345",
        )
    assert str(exc_info.value) == "Member ID must be a 9-digit number."

@pytest.mark.parametrize("invalid_name", ["", "A" * 51])
def test_update_member_invalid_name(test_db, invalid_name):
    
    # Add a valid member
    member = mc.add_member(
        name="Valid Name",
        street_address="1111 Valid St",
        city="Validville",
        state="VV",
        zip_code="66666",
        status="A",
    )
    
    # Attempt to update the member with an invalid name
    with pytest.raises(exc.FieldValueError) as exc_info:
        mc.update_member(
            member_id=member.member_id,
            name=invalid_name,
            street_address="2222 Updated St",
            city="Updatedville",
            state="UU",
            zip_code="77777",
        )
    assert str(exc_info.value) == "Name must be between 1 and 50 characters long."

@pytest.mark.parametrize("invalid_street_address", ["", "A" * 4, "A" * 101])
def test_update_member_invalid_street_address(test_db, invalid_street_address):
    
    # Add a valid member
    member = mc.add_member(
        name="Valid Name",
        street_address="1111 Valid St",
        city="Validville",
        state="VV",
        zip_code="66666",
        status="A",
    )
    
    # Attempt to update the member with an invalid street address
    with pytest.raises(exc.FieldValueError) as exc_info:
        mc.update_member(
            member_id=member.member_id,
            name="Updated Name",
            street_address=invalid_street_address,
            city="Updatedville",
            state="UU",
            zip_code="77777",
        )
        
    assert (
        str(exc_info.value)
        == "Street address must be between 5 and 100 characters long."
    )

@pytest.mark.parametrize("invalid_city", ["", "A" * 26])
def test_update_member_invalid_city(test_db, invalid_city):
    
    # Add a valid member
    member = mc.add_member(
        name="Valid Name",
        street_address="1111 Valid St",
        city="Validville",
        state="VV",
        zip_code="66666",
        status="A",
    )
    
    # Attempt to update the member with an invalid city
    with pytest.raises(exc.FieldValueError) as exc_info:
        mc.update_member(
            member_id=member.member_id,
            name="Updated Name",
            street_address="2222 Updated St",
            city=invalid_city,
            state="UU",
            zip_code="77777",
        )
    assert str(exc_info.value) == "City must be between 1 and 25 characters long."

@pytest.mark.parametrize("invalid_state", ["", "A", "AAA"])
def test_update_member_invalid_state(test_db, invalid_state):
    
    # Add a valid member
    member = mc.add_member(
        name="Valid Name",
        street_address="1111 Valid St",
        city="Validville",
        state="VV",
        zip_code="66666",
        status="A",
    )
    
    # Attempt to update the member with an invalid state
    with pytest.raises(exc.FieldValueError) as exc_info:
        mc.update_member(
            member_id=member.member_id,
            name="Updated Name",
            street_address="2222 Updated St",
            city="Updatedville",
            state=invalid_state,
            zip_code="77777",
        )
    assert str(exc_info.value) == "State must be a 2-character abbreviation."

@pytest.mark.parametrize("invalid_zip_code", ["", "1234", "123456", "ABCDE", "A1234"])
def test_update_member_invalid_zip_code(test_db, invalid_zip_code):
    
    # Add a valid member
    member = mc.add_member(
        name="Valid Name",
        street_address="1111 Valid St",
        city="Validville",
        state="VV",
        zip_code="66666",
        status="A",
    )
    
    # Attempt to update the member with an invalid zip code
    with pytest.raises(exc.FieldValueError) as exc_info:
        mc.update_member(
            member_id=member.member_id,
            name="Updated Name",
            street_address="2222 Updated St",
            city="Updatedville",
            state="UU",
            zip_code=invalid_zip_code,
        )
    assert str(exc_info.value) == "Zip code must be a 5-digit number."

def test_delete_member_valid(test_db):
    # Add a valid member
    member = mc.add_member(
        name="Valid Name",
        street_address="1111 Valid St",
        city="Validville",
        state="VV",
        zip_code="66666",
        status="A",
    )
    
    # Delete the member
    mc.delete_member(member.member_id)
    
    # Verify that the member cannot be retrieved through the controller
    deleted_member = mc.get_member_by_id(member.member_id)
    assert deleted_member is None
    
    # Verify that the member still exists in the database
    deleted_member = Members.get_by_id(member.member_id)
    assert deleted_member.is_deleted is True
    assert Members.select().count() == 1

def test_delete_member_nonexistent(test_db):
    
    # Attempt to delete a member that does not exist
    with pytest.raises(exc.MemberNotFound) as exc_info:
        mc.delete_member("000000999")
        
    assert str(exc_info.value) == "Member with ID 000000999 does not exist."

def test_delete_member_soft_deleted(test_db):
    # Add a valid member
    member = mc.add_member(
        name="Valid Name",
        street_address="1111 Valid St",
        city="Validville",
        state="VV",
        zip_code="66666",
        status="A",
    )
    
    # Soft delete the member
    mc.delete_member(member.member_id)
    
    # Attempt to delete the same member again
    with pytest.raises(exc.MemberNotFound) as exc_info:
        mc.delete_member(member.member_id)
        
    assert str(exc_info.value) == f"Member with ID {member.member_id} does not exist."
    
    # Verify that the member still exists in the database
    deleted_member = Members.get_by_id(member.member_id)
    assert deleted_member.is_deleted is True
    assert Members.select().count() == 1
