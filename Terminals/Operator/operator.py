# This will be the main entry point of the operator program!
class Operator:
    
    def get_operator_option(self) -> int:
        option = 0
        
        while option <= 0 or option > 7:
            print("\n\nAvailable options for Operators:")
            print("1. Add member.")
            print("2. Remove member.")
            print("3. Update member information")
            print("-----------------------------")
            print("4. Add provider")
            print("5. Remove provider")
            print("6. Update provider information")
            print("-----------------------------")
            print("7. Return back to main menu.\n")
            
            option = int(input("Enter your choice [1-7]: "))
            
            if option <= 0 or option > 7:
                print("Invalid option. Please enter [1-7].")
        
        return option
    
    def operator_interface(self):
        option = 0
        #An instance of Operator Service goes here
        #operator_service = Operator_Service() 
        
        while option != 7:
            option = self.get_operator_option()
            
            match option:
                case 1:
                    print("You chose to add a new member. Enter following information.")
                    name = input("Enter member name: ")
                    street_address = input("Enter member's street address: ")
                    city = input("Enter member's city: ")
                    state = input("Enter member's state (2 letters): ")
                    zip_code = input("Enter member's zip code: ")                        
                    """
                    if operator_service.add_member(name, street_address,
                       city, state, zip_code) is not False:
                        print("Member successfuly added.")
                    else:
                        print("Failed to add. Try again.")
                    """
                case 2:
                    print("You chose to remove member.")
                    member_id = input("Enter member number (9 digits): ")
                    """
                    if operator_service.remove_member(member_id) is not False:
                        print("Member removed successfuly")
                    else:
                        print("Failed to remove member with id: ", member_id)        
                    """ 
                
                case 3:
                    print("You chose to update member information.")

                    member_id = input("Enter member number (9 digits): ")
                    """
                    if operator_service.validate_member(member_id ) is not False:
                        name = input("Enter updated member name: ")
                        street_address = input("Enter updated member's street address: ")
                        city = input("Enter updated member's city: ")
                        state = input("Enter updated member's state (2 letters): ")
                        zip_code = input("Enter updated member's zip code: ")    
                    else:
                        print("Member doesn't exist. Enter valid number.")
                    """
                case 4:
                    print("You chose to add a new provider. Enter following information.")
                    provider_name = input("Enter new provider's name: ")
                    provider_address = input("Enter provider's address: ")
                    provider_city = input("Enter provider's city: ")
                    provider_state = input("Enter provider's state (2 letters): ")
                    provider_zipcode = input("Enter provider's zipcode: ")
                    
                    """
                    if operator_service.add_provider(provider_name, provider_address, provider_city,
                        provider_state, provider_zipcode) is not False:
                        print("Provider successfuly added.")
                    else:
                        print("Failed to add.")
                    """
                case 5:
                    print("You chose to remove provider.")
                    provider_id = input("Enter provider number (9 digits): ")
                    
                    """
                    if operator_service.remove_provider(provider_id) is not False:
                        print("Provider successfuly removed")
                    else:
                        print("Failed to remove provider with id: ", provider_id)
                    """
                case 6:
                    print("You chose to update provider information.")
                    provider_id = input("Enter provider's number (9 digits): ")
                    """
                    if operator_service.validate_provider() is not False:
                        provider_name = input("Enter provider's updated name: ")
                        provider_address = input("Enter provider's updated address: ")
                        provider_city = input("Enter provider's updated city: ")
                        provider_state = input("Enter provider's updated state (2 letters): ")
                        provider_zipcode = input("Enter provider's updated zipcode: ")
                    
                    else:
                        print("Invalid provider number. Try again.")
                    """
                