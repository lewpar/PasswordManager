def add_credential():
    print("test")
    pass


def view_credential():
    pass


menu_options = {
    0: ("Add Credentials", add_credential),
    1: ("View Credentials", view_credential)
}


def write_menu():
    print("=============================")
    print("|| DigiCore Password Vault ||")
    print("=============================")
    
    # Iterate over the menu items dictionary
    # to render the menu item names & index.
    for i in range(0, len(menu_options)):
        menu_title, _ = menu_options[i]
        print(f"|| {i}) {menu_title}")
        
    print("=============================")
    user_input = input("|| Enter menu option (number): ")
    print("=============================")
    
    return user_input


# The entry-point of the application,
# where the main execution begins for the application.
def main():
    # Display the user menu and return user input
    user_input = write_menu()
    menu_title, menu_function = menu_options[int(user_input)]
    print(f"Found: {menu_title}")
    menu_function()


# If the application is imported as a module,
# this stops any code from running that was intended for direct execution.
if __name__ == "__main__":
    main()