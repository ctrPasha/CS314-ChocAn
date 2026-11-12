from peewee import Check, CharField
from database.base_model import BaseModel

class Providers(BaseModel):
    provider_id = CharField(
		primary_key= True,
		max_length= 9,
		constraints = [
			Check("LENGTH(provider_id) = 9"),
   			Check("provider_id NOT GLOB '*[^0-9]*'"),
		]
	)
    
    name = CharField(
        max_length= 25,
        constraints= [
			Check("LENGTH(name) <= 25")
		]
    )
    
    address = CharField(
		max_length = 25,
		constraints= [
			Check("LENGTH(address) <= 25")
		]
	)
    
    city = CharField(
        max_length= 14,
        constraints= [
			Check("LENGTH(city) <= 14")
		]
	)
    
    state = CharField(
		max_length= 2,
		constraints= [
			Check("LENGTH(state) = 2")
		]
	)
    
    zip_code = CharField(
        max_length= 5,
        constraints= [
			Check("LENGTH(zip_code) = 5"),
			Check("zip_code NOT GLOB '*[^0-9]*'"),
		]
	)
    
    class Meta:
        table_name = "Providers"