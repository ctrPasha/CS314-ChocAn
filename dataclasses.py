"""
This module contains data package classes that are designed to allow the calling method to easily
pass data into the service modules.
"""
from dataclasses import dataclass

@dataclass
class PersonData:
    name: str
    street_address: str
    city: str
    state: str
    zip_code: str