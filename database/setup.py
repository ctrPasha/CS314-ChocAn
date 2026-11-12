from database.connection import db
from database.members.members_model import Members
from database.providers.providers_model import Providers
from database.service_records.service_records_model import ServiceRecords
from database.services.services_model import Services

def setup_database():
    with db:
        db.create_tables(
            [Members, Services, Providers, ServiceRecords], 
        	safe=True
        )

    print("Database tables created successfully!")

if __name__ == "__main__":
    setup_database()