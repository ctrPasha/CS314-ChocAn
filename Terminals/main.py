# This will be the main entr
from Operator.operator import Operator

        
def main():
    run_main_menu()

def run_main_menu():
    # Main Terminal Interface (main menu)    
    option = 0

    while option != 5:
        option = get_option()
        match option:
            case 1:
                #create an instance of Provider (class)
                #call provider's menu/interface
                pass
                            
            case 2:
                operator = Operator()
                operator.operator_interface()
            
            case 3:
                #create an instance of Manager (class)
                #call manager's menu/interface
                pass
                
            case 4:
                #instruction_message()
                pass
    
    print("Exiting...")
        
    
 
def get_option() -> int:
    option = 0
    while option <= 0 or option > 5:
        print("\n\nAvailable options:")
        print("1. Enter as Provider")
        print("2. Enter as Operator")
        print("3. Enter as Manager")
        print("4. Usage instructions")
        print("5. Quit\n")
        
        option = int(input("Enter your choice [1-5]: "))
        
        if option <= 0 or option > 5:
            print("Invalid option. Please enter [1-5].\n")
    
    return option

   
if __name__ == "__main__":
    main()