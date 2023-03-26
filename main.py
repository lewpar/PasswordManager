# Imports the OS related functions, like reading and writing to disk.
import os

# Imports the serialization tools, otherwise known as 'pickling'.
# This allows me to write class objects to disk.
import pickle

# Imports the crypto.py file I created.
import crypto

# Imports the sleep function so I can sleep on first load
# of the application.
from time import sleep

# Imports the vaultmgr.py file I created,
# only importing the two types I created.
from vaultmgr import VaultManager, VaultEntry

# Path variables for the vault and log file.
PATH_VAULT = "./vault"
PATH_VAULT_FILE = f"{PATH_VAULT}/vault.vlt"
PATH_LOG = "./log.txt"

# The Caeser Cipher shift value.
ROT_CIPHER_SHIFT = 3

# The vault manager class instance.
vault_mgr: VaultManager

# The flag to detect when to exit the program from menu.
exit_requested = False


# Clears the console screen.
def console_clear():
    # If the system is Windows, use the cls command.
    if os.name == "nt":
        _ = os.system("cls")
    # Otherwise, it's likely macOS or Linux. Use the clear command.
    else:
        _ = os.system("clear")


def dump_log(log):
    with open(PATH_LOG, "at") as log_file:
        log_file.write(f"{str(log)}\r\n")


def vault_save():
    # Write a new VaultManager file to disk. Using mode 'wb' -> 'write', 'binary'
    with open(PATH_VAULT_FILE, "wb") as vault_file:
        # Serialize the VaultManager to a byte array.
        pickle.dump(vault_mgr, vault_file)
        
    
# Check if the entry is already present in the vault.    
def is_in_vault(vault_entry: VaultEntry):
    for entry in vault_mgr.vault:
        if entry.username.lower() == vault_entry.username.lower() and entry.website.lower() == vault_entry.website.lower():
            return True
        
    return False


# Prompt the user to overwrite existing vault credentials.
def prompt_overwrite(vault_entry: VaultEntry):
    print()
    print("|| These credentials are already present in the vault.")
    print("|| Do you want to overwrite?")
    print()
    print("|| 0) No")
    print("|| 1) Yes")
    print()
    
    user_input = ""
    
    # Loops until the user enters either '0' or '1'.
    while(True):
        user_input = input("> ").strip()
        if user_input == "0" or user_input == "1":
            break
    
    # Using a Ternary Operator to return True or False based on user_input.
    return True if user_input == "1" else False


# Prompt the user to add a new credential to the vault.
def add_credential():
    username = input("|| Username: ")
    password = input("|| Password: ")
    website = input("|| Website: ")

    # Encrypt the password using the Caeser Cipher, shifted by 3 to the right.
    password_encrypted = crypto.Rot.encrypt(password, ROT_CIPHER_SHIFT)

    # Create a new vault entry with the encrypted password.
    new_vault_entry = VaultEntry(username, password_encrypted, website)
    
    # Used later to detect if anything has changed and should save the vault.
    should_save = False
    
    # Check is the credentials are already present in the vault.
    if not is_in_vault(new_vault_entry):
        # Add the credentials to the vault.
        vault_mgr.add_entry(new_vault_entry)
        should_save = True
    else:
        overwrite = prompt_overwrite(new_vault_entry)
        
        # Overwrite the entry if user chose 'yes' to overwrite.
        if overwrite:
            vault_mgr.overwrite_entry(new_vault_entry)
            should_save = True
    
    # Flag on whether the vault should be saved to disk,
    # saves on disk writes when you haven't changed anything.
    if should_save:
        # Save the vault to file.
        vault_save()

        print()
        print(f"|| Credentials stored, password was encrypted as '{password_encrypted}'.")
        print()

    # Prompt the user to return to menu and discard any input received.
    _ = input("Press <ENTER> to return to main menu.")


# Prompt the user with credentials in the vault.
def view_credential():
    # If there are no credentials in the vault, prompt the user to make one.
    if len(vault_mgr.vault) < 1:
        print()
        print("No credentials found, navigate to 'Add Credentials' on the menu to create one")
        print()
        _ = input("Press <ENTER> to return to main menu.")
        return
    
    print("|| Format: username : password : website")
    print()
    # Iterate over the credentials in the vault and print them.
    for i in range(len(vault_mgr.vault)):
        entry = vault_mgr.vault[i]
        print(f"|| {i}) {entry.username} : {crypto.Rot.decrypt(entry.password, ROT_CIPHER_SHIFT)} : {entry.website}")

    print()
    print("To remove an entry, type 'delete' followed by the entry number.")
    print("Example: delete 1")
    print()
    print("Otherwise, type 'quit' to return to menu.")
    print()
    
    entry_deleted = False
    
    while True:
        user_input = input("> ").strip()
        
        if user_input.lower() == "quit":
            break
        
        elif user_input.lower().startswith("delete"):
            try: 
                # Convert the second item in split to an integer.
                entry_index = int(user_input.split(' ')[1])
                
                # The deletion index is higher than the amount of credentials in the vault.
                # Continue to next loop and re-prompt.
                if entry_index > len(vault_mgr.vault) or entry_index < 0:
                    print("Invalid entry index.")
                    continue
                
                # Delete entry, set flag, then break out of the loop.
                del vault_mgr.vault[entry_index]
                entry_deleted = True
                break
            
            except ValueError or KeyError:  # Catch errors, continue and re-prompt.
                print("Invalid input.")
                continue
            
    # If an entry was deleted, we want to refresh the credentials.
    # Save credentials to disk, clear screen, and re-open the credentials screen.
    if entry_deleted:
        vault_save()
        _ = input("Deleted entry, press <ENTER> to return to main menu.")


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


# Load the vault from disk into the vault_mgr instance.
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

        # Just prompts the user on where the vault is created on disk.
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


# Prompt the user with the main menu.
def write_menu():
    print("=============================")
    print("|| DigiCore Password Vault ||")
    print("=============================")
    
    # Iterate over the menu items dictionary
    # to render the menu item titles & index.
    for i in range(0, len(menu_options)):
        menu_title, _ = menu_options[i]
        print(f"|| {i}) {menu_title}")
        
    print()
    user_input = input("|| Enter menu option (number): ")
    print()
    
    return user_input


# The entry-point of the application,
# where the main execution begins for the application.
def main():
    # Load the user password vault
    load_vault()

    # Loop the menu until exit has been requested.
    while not exit_requested:
        # Clear the screen to remove the vault load text / previous menus, if any.
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
        except ValueError or KeyError:  # Ignore value/key errors and re-prompt menu.
            pass
        except Exception as ex:  # Unexpected error occurred, log to file.
            print("An error occurred trying to execute a menu function with exception:")
            print(ex)
            print("Contact your supervisor to report the issue.")
            print(f"Dumping error to '{PATH_LOG}'.")
            dump_log(ex)
            input()


# If the application is imported as a module,
# this stops any code from running that was intended for direct execution.
if __name__ == "__main__":
    main()
