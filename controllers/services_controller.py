from database.services.services_model import Services

def get_services_by_code(service_code: str) -> Services | None:
	"""
    Retrieve a service from the database based on the service_code entered.
    If the service exists, return the service object (row) else return None.
    """
    
	return Services.get_or_none(
    	(Services.service_code == service_code) & (Services.is_deleted == False)
    )

def add_service(service_code: str, service_name: str, fee: float) -> None:
	"""
	Add a new service to the database.
	Raises ValueError if the service already exists or if the fee is invalid.
	"""
 
	if len(service_code) != 6 or not service_code.isdigit():
		raise ValueError("Service code must be a 6-digit number.")

	if not 1 <= len(service_name) <= 50:
		raise ValueError("Service name must be between 1 and 50 characters long.")
 
	if Services.get_or_none(Services.service_code == service_code) is not None:
		raise ValueError(f"Service with code {service_code} already exists.")
 
	if fee < 0.00 or fee > 999.99:
		raise ValueError("Fee must be between 0.00 and 999.99.")
 
	return Services.create(
		service_code = service_code,
		service_name = service_name,
		fee = fee
	)

def update_service_fee(service_code: str, new_fee: float) -> None:
	"""
	Update the fee of a service in the database.
	
	Saves the update if the service exists and the new fee is valid (between 0.00 and 999.99).
	Raises ValueError if the service does not exist or if the new fee is invalid.
	"""
 
	if new_fee < 0.00 or new_fee > 999.99:
		raise ValueError("Fee must be between 0.00 and 999.99.")
 
	service = get_services_by_code(service_code)
	
	if service is None:
		raise ValueError(f"Service with code {service_code} does not exist.")
 
	service.fee = new_fee
	service.save()
 
def delete_service(service_code: str) -> None:
	"""
	Delete a service from the database.
	
	Raises ValueError if the service does not exist.
	"""
 
	service = get_services_by_code(service_code)
	
	if service is None:
		raise ValueError(f"Service with code {service_code} does not exist.")
 
	service.is_deleted = True
	service.save()