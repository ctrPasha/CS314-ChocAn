from database.providers.providers_model import Providers

def generate_provider_id() -> str:
    """
    Generate a unique 9-digit provider ID.
    """
    last_provider = Providers.select().order_by(Providers.provider_id.desc()).first()
    
    if last_provider is None:
        return "000000001"
    
    next_id = int(last_provider.provider_id) + 1
    
    if next_id > 999999999:
        raise ValueError("Provider ID limit reached. Cannot generate a new provider ID.")
    
    return f"{next_id:09d}"

def get_provider_by_id(provider_id: str) -> Providers | None:
	"""
	Retrieve a provider from the database based on the provider_id entered.
	If the provider exists, return the provider object (row) else return None.
	"""
	
	return Providers.get_or_none(
    	(Providers.provider_id == provider_id) & (Providers.is_deleted == False)
	)

def add_provider(name: str, street_address: str, city: str, state: str, zip_code: str) -> Providers:
	"""
	Add a new provider to the database.
	Returns the newly created provider object.
	Raises ValueError if provider information is invalid or the ID limit is reached.	
	"""

	if len(name) < 1 or len(name) > 25:
		raise ValueError("Provider name must be between 1 and 25 characters long.")

	if len(street_address) < 1 or len(street_address) > 25:
		raise ValueError("Street address must be between 1 and 25 characters long.")

	if len(city) < 1 or len(city) > 14:
		raise ValueError("City must be between 1 and 14 characters long.")

	if len(state) != 2:
		raise ValueError("State must be a 2-character abbreviation.")

	if len(zip_code) != 5 or not zip_code.isdigit():
		raise ValueError("Zip code must be a 5-digit number.")
  	
	# Use a transaction to group ID generation and provider creation
		# into one database operation, rolling back on failure.
	with Providers._meta.database.atomic():
		provider_id = generate_provider_id()
   
		return Providers.create(
			provider_id = provider_id,
			name = name,
			address = street_address,
			city = city,
			state = state,
			zip_code = zip_code
		)

def update_provider(provider_id: str, name: str, street_address: str, city: str, state: str, zip_code: str) -> None:
	"""
	Update an existing provider in the database.
	Raises ValueError if the provider does not exist or if any of the provided values are invalid.
	"""
	if len(provider_id) != 9 or not provider_id.isdigit():
		raise ValueError("Provider ID must be a 9-digit number.")

	provider = get_provider_by_id(provider_id)
	
	if provider is None:
		raise ValueError(f"Provider with ID {provider_id} does not exist.")

	if len(name) < 1 or len(name) > 25:
		raise ValueError("Provider name must be between 1 and 25 characters long.")

	if len(street_address) < 1 or len(street_address) > 25:
		raise ValueError("Street address must be between 1 and 25 characters long.")

	if len(city) < 1 or len(city) > 14:
		raise ValueError("City must be between 1 and 14 characters long.")

	if len(state) != 2:
		raise ValueError("State must be a 2-character abbreviation.")

	if len(zip_code) != 5 or not zip_code.isdigit():
		raise ValueError("Zip code must be a 5-digit number.")

	
	provider.name = name
	provider.address = street_address
	provider.city = city
	provider.state = state
	provider.zip_code = zip_code	
	provider.save()
 

def delete_provider(provider_id: str) -> None:
	"""
	Delete a provider from the database.
	
	Raises ValueError if the provider does not exist.
	"""
	provider = get_provider_by_id(provider_id)
	
	if provider is None:
		raise ValueError(f"Provider with ID {provider_id} does not exist.")

	provider.is_deleted = True
	provider.save()
