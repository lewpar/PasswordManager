import os
import pickle
import crypto

from time import sleep
from vaultmgr import VaultManager, VaultEntry

PATH_VAULT = "./vault"
PATH_VAULT_FILE = f"{PATH_VAULT}/vault.vlt"

ROT_CIPHER_SHIFT = 3

vault_mgr: VaultManager
exit_requested = False


# Clears the console screen.
def console_clear():
    # If the system is windows, use the cls command.
    if os.name == "nt":
        _ = os.system("cls")
    # Otherwise it's likely macOS or Linux, use the clear command.
    else:
        _ = os.system("clear")


def vault_save():
    # Write a new VaultManager file to disk. Using mode 'wb' -> 'write', 'binary'
    with open(PATH_VAULT_FILE, "wb") as vault_file:
        # Serialize the VaultManager to a byte array.
        pickle.dump(vault_mgr, vault_file)


def add_credential():
    username = input("|| Username: ")
    password = input("|| Password: ")
    website = input("|| Website: ")
    password_encrypted = crypto.Rot.encrypt(password, ROT_CIPHER_SHIFT)

    vault_mgr.add_entry(VaultEntry(username, password, website))

    print("=============================")
    print(f"|| Credentials stored, password was encrypted as '{password_encrypted}'.")
    print("=============================")
    # Prompt the user to return to menu and discard any input received.
    _ = input("Press <ENTER> to return to menu.")


def view_credential():
    print(vault_mgr.vault)
    for entry in vault_mgr.vault:
        print(f"|| {entry.username} : {entry.password} : {entry.website}")

    # Prompt the user to return to menu and discard any input received.
    _ = input("Press <ENTER> to return to menu.")


def request_exit():
    global exit_requested
    exit_requested = True
    pass


# The menu options that are selected by the key,
# the key is selected from user input.
# The value in the dictionary is a tuple containing the
# title of the menu option and the pointer to related function.
menu_options = {
    0: ("Add Credentials", add_credential),
    1: ("View Credentials", view_credential),
    2: ("Quit", request_exit)
}


def load_vault():
    # Make the vault_mgr global variable
    # writable from local scope.
    global vault_mgr

    # Check if the Vault File exists.
    if not os.path.isfile(PATH_VAULT_FILE):
        print("No vault found, creating new..")

        # Vault path doesn't exist, create directory.
        if not os.path.exists(PATH_VAULT):
            os.mkdir(PATH_VAULT)

        print(f"Created vault at '{os.path.realpath(PATH_VAULT_FILE)}'.")

        # Create a new instance of the Vault Manager class.
        vault_mgr = VaultManager()
        vault_save()

        print("Entering main menu..")
        sleep(2.5)

    # Vault does exist
    else:
        # Read the vault file from disk. Using mode 'rb' -> 'read', 'binary'
        with open(PATH_VAULT_FILE, "rb") as vault_file:
            # Deserialize the vault file back into an instance of
            # VaultManager.
            vault_mgr = pickle.load(vault_file)


def write_menu():
    print("=============================")
    print("|| DigiCore Password Vault ||")
    print("=============================")
    
    # Iterate over the menu items dictionary
    # to render the menu item titles & index.
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
    # Load the user password vault
    load_vault()

    # Clear the screen to remove the vault load text, if any.
    console_clear()

    # Display the user menu and return user input
    user_input = write_menu()
    
    try:
        # Get the tuple result from the menu dictionary,
        # containing the title and function pointer.
        menu_title, menu_function = menu_options[int(user_input)]

        # Clear the screen for the menu option.
        console_clear()

        # Display the title of the menu selected
        print("=============================")
        print(f"|| {menu_title}")
        print("=============================")

        # Call the function tied to the menu selected.
        menu_function()
    except:
        # Invalid option selected
        print("Invalid option, returning to menu.")

    # Return to main-menu if not exiting.
    if not exit_requested:
        main()


# If the application is imported as a module,
# this stops any code from running that was intended for direct execution.
if __name__ == "__main__":
    main()
