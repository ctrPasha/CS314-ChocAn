from database.service_records.service_records_model import ServiceRecords
from controllers import member_controllers as mc
from controllers import providers_controller as pc
from controllers import services_controller as sc
import datetime

def get_service_record_by_id(record_id: int) -> ServiceRecords | None:
	"""
	Retrieve a service record from the database based on the record_id entered.
	If the service record exists, return the service record object (row) else return None.
	"""
 
	return ServiceRecords.get_or_none(
		(ServiceRecords.record_id == record_id) & (ServiceRecords.is_deleted == False)
	)

def get_service_records_by_member(member_id: str) -> list[ServiceRecords]:
	"""
	Retrieve all service records for a specific member from the database based on the member_id entered.
	If the member has service records, return a list of service record objects (rows) else return an empty list.
	"""
 
	return list(ServiceRecords.select().where(
		(ServiceRecords.member == member_id) & (ServiceRecords.is_deleted == False)
	))

def add_service_record(service_date: datetime.date, provider: str, member: str, 
                       service_code: str, comments: str | None = None) -> ServiceRecords:
	"""
	Add a new service record to the database.
	Returns the created service record
	"""
	
	if not isinstance(service_date, datetime.date) or isinstance(
        service_date, datetime.datetime
    ):
		raise ValueError("Service date must be a valid date.")

	if provider is None or not provider:
		raise ValueError("Provider ID must be provided.")

	if member is None or not member:
		raise ValueError("Member ID must be provided.")

	if service_code is None or not service_code:
		raise ValueError("Service code must be provided.")

	if comments is not None and len(comments) > 100:
		raise ValueError("Comments must be 100 characters or fewer.")

	if not mc.validate_member(member):
		raise ValueError(f"Member with ID {member} is not valid.")

	provider_obj = pc.get_provider_by_id(provider)
 
	if provider_obj is None:
		raise ValueError(f"Provider with ID {provider} does not exist.")

	service = sc.get_services_by_code(service_code)
 
	if service is None:
		raise ValueError(f"Service with code {service_code} does not exist.")

	service_record = ServiceRecords.create(
		service_date=service_date,
		provider=provider_obj,
		member=member,
		service_code=service,
		comments=comments,
  		fee=service.fee	
	)
 
	return service_record

def get_records_by_provider(provider_id: str) -> list[ServiceRecords]:
	"""
	Retrieve all service records for a specific provider from the database based on the provider_id entered.
	If the provider has service records, return a list of service record objects (rows) else return an empty list.
	"""
 
	return list(ServiceRecords.select().where(
		(ServiceRecords.provider == provider_id) & (ServiceRecords.is_deleted == False)
	))
 
def get_records_by_date_range(start_date: datetime.datetime, end_date: datetime.datetime) -> list[ServiceRecords]:
	"""
	Retrieve all service records within a specific date range from the database.
	If there are service records in the date range, return a list of service record objects (rows) else return an empty list.
	"""
	
	if not isinstance(start_date, datetime.datetime):
		raise ValueError("Start date must be a valid datetime.")

	if not isinstance(end_date, datetime.datetime):
		raise ValueError("End date must be a valid datetime.")	
 
	if start_date >= end_date:
		raise ValueError("Start date must be earlier than end date.")

 
	return list(ServiceRecords.select().where(
		(ServiceRecords.recorded_at >= start_date) & 
  		(ServiceRecords.recorded_at < end_date) & 
    	(ServiceRecords.is_deleted == False)
	))

def get_all_service_records() -> list[ServiceRecords]:
	"""
	Retrieve all service records from the database.
	If there are service records, return a list of service record objects (rows) else return an empty list.
	"""
 
	return list(ServiceRecords.select().where(ServiceRecords.is_deleted == False))
