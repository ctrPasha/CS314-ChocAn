from peewee import Check, CharField, DoubleField
from database.base_model import BaseModel

class Services(BaseModel):
    service_code = CharField(
		primary_key = True,
		max_length = 6,
		constraints = [
			Check("LENGTH(service_code) = 6"),
			Check("service_code NOT GLOB '*[^0-9]*'"),
		]
	)
    
    service_name = CharField(max_length= 50)
    
    fee = DoubleField(
		constraints = [
			Check("fee >= 0.00 AND fee <= 999.99")
		]
	)

    class Meta:
        table_name = "Services"