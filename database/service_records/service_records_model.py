import datetime

from peewee import Check, DateTimeField, CharField, DateField, ForeignKeyField, DoubleField, AutoField
from database.base_model import BaseModel
from database.members.members_model import Members
from database.providers.providers_model import Providers
from database.services.services_model import Services

class ServiceRecords(BaseModel):
    record_id = AutoField(
		primary_key = True,
  	)
    
    recorded_at = DateTimeField(default = datetime.datetime.now)
    
    service_date = DateField()

    provider = ForeignKeyField(
        Providers,
        backref = "provider_id",
        on_delete = "RESTRICT",
    )

    member = ForeignKeyField(
		Members,
		backref = "member_id",
		on_delete = "RESTRICT",
	)
    
    service_code = ForeignKeyField(
		Services,
 		column_name="service_code",
		backref = "service_code",
		on_delete = "RESTRICT",
	)
    
    comments = CharField(
        max_length = 100,
        null = True,
        constraints = [
            Check("LENGTH(comments) <= 100")
		]
	)
    
    fee = DoubleField(
		constraints = [
			Check("fee >= 0.00 AND fee <= 999.99")
		]
	)
    
    class Meta:
        table_name = "ServiceRecords"
    
    