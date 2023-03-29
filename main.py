# Supervisor Sign-off

# Imports the OS related functions, like reading and writing to disk.
import os

# Imports the shutil for delete a whole directory tree.
import shutil

# Imports the crypto.py file I created.
import crypto

# Imports the config parser for reading config files.
import configparser

# Imports the datetime functions.
from datetime import datetime

# Imports the vaultmgr.py file I created,
# only importing the two types I created.
from vaultmgr import VaultManager, VaultEntry

# Path variables for the vault, config, and log file.
PATH_VAULT = "./vault"
PATH_VAULT_FILE = "/vault.vlt"
PATH_CONFIG = "./config.ini"
PATH_LOG = "./log.txt"

# The Caeser Cipher shift value.
ROT_CIPHER_SHIFT = 0

# The configuration instance
config: configparser.ConfigParser

# The vault manager class instance.
vault_mgr: VaultManager

# The flag to detect when to exit the program from menu.
exit_requested = False


# Formats the vault file location.
def vault_file_loc():
    return f"{PATH_VAULT}{PATH_VAULT_FILE}"


# Clears the console screen.
def console_clear():
    # If the system is Windows, use the cls command.
    if os.name == "nt":
        _ = os.system("cls")
    # Otherwise, it's likely macOS or Linux. Use the clear command.
    else:
        _ = os.system("clear")


# Dumps an error to the log file on disk.
def dump_log(log):
    # If the log file is moved to a new directory that doesn't exist, create it.
    if not os.path.isfile(PATH_LOG):
        os.makedirs(os.path.dirname(PATH_LOG), exist_ok=True)
        
    with open(PATH_LOG, "at") as log_file:
        log_file.write(f"[{datetime.now()}]: {str(log)}\r\n")
        
    
# Check if the entry is already present in the vault.    
def is_in_vault(vault_entry: VaultEntry):
    for entry in vault_mgr.vault:
        if entry.username.lower() == vault_entry.username.lower() and \
                entry.resource.lower() == vault_entry.resource.lower():
            return True
        
    return False


# Prompt the user to overwrite existing vault credentials.
def prompt_overwrite():
    print()
    print("|| These credentials are already present in the vault.")
    print("|| Do you want to overwrite?")
    print()
    print("|| 0) No")
    print("|| 1) Yes")
    print()
    
    user_input = ""
    
    # Loops until the user enters either '0' or '1'.
    while True:
        user_input = input("> ").strip()
        if user_input == "0" or user_input == "1":
            break
    
    # Using a Ternary Operator to return True or False based on user_input.
    return True if user_input == "1" else False


# Prompt the user to add a new credential to the vault.
def add_credential():
    username, password, resource = ("", "", "")
    
    # The amount of tries the user has attempted.
    tries = 0
    
    # Loop until all entries are populated with a value.
    while username == "" or password == "" or resource == "":
        if tries > 0:
            # Clear the entries to prevent caching which allows
            # a desync between display and actual value.
            username, password, resource = ("", "", "")
            print()
            print("You must enter a value for all entries.")
            print()
            
        username = input("|| Username: ").strip()
        password = input("|| Password: ").strip()
        resource = input("|| Resource: ").strip()
        
        # Increment tries for next loop.
        tries += 1

    # Encrypt the password using the Caeser Cipher, shifted by 3 to the right.
    password_encrypted = crypto.Rot.encrypt(password, ROT_CIPHER_SHIFT)

    # Create a new vault entry with the encrypted password.
    new_vault_entry = VaultEntry(username, password_encrypted, resource)
    
    # Used later to detect if anything has changed and should save the vault.
    should_save = False
    
    # Check is the credentials are already present in the vault.
    if not is_in_vault(new_vault_entry):
        # Add the credentials to the vault.
        vault_mgr.add_entry(new_vault_entry)
        should_save = True
    else:
        overwrite = prompt_overwrite()
        
        # Overwrite the entry if user chose 'yes' to overwrite.
        if overwrite:
            vault_mgr.overwrite_entry(new_vault_entry)
            should_save = True
    
    # Flag on whether the vault should be saved to disk,
    # saves on disk writes when you haven't changed anything.
    if should_save:
        # Save the vault to file.
        vault_mgr.vault_save()

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
        
        # Prompt the user to return to menu and discard any input received.
        _ = input("Press <ENTER> to return to main menu.")
        return
    
    # The padding values for the formatted strings below.
    alignment_padding = 15
    alignment_padding_entry = 10
    
    print(f"|| {'entry' : <{alignment_padding_entry}} : {'username' : <{alignment_padding}} : {'password' : <{alignment_padding}} : {'resource' : <{alignment_padding}}")
    print()
    
    # Iterate over the credentials in the vault and print them.
    for i in range(len(vault_mgr.vault)):
        entry = vault_mgr.vault[i]
        print(f"|| {i : <{alignment_padding_entry}} : {entry.username : <{alignment_padding}} : {crypto.Rot.decrypt(entry.password, ROT_CIPHER_SHIFT) : <{alignment_padding}} : {entry.resource : <{alignment_padding}}")

    # It should display 'entry' instead of 'entries' when there are less than 2 credentials.
    entry_string = "entries" if len(vault_mgr.vault) > 1 else "entry"
    
    print()
    print(f"|| '{len(vault_mgr.vault)}' {entry_string} found in the Vault.")
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
                # Store the arguments for the delete command
                delete_args = user_input.split(' ')
                
                # Check that at least 1 argument has been passed,
                # but no more than 1.
                if len(delete_args) != 2:
                    print("Invalid arguments.")
                    continue
                
                # Convert the second item in split to an integer.
                entry_index = int(delete_args[1])
                
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
        vault_mgr.vault_save()
        _ = input("Deleted entry, press <ENTER> to return to main menu.")


# Sets the exit_requested flag to tell the main
# menu loop to exit the application.
def request_exit():
    global exit_requested
    exit_requested = True
    pass


# The menu options that are selected by the key,
# the key is selected from user input.
# The value in the dictionary is a tuple containing the
# title of the menu option and the pointer to related function.
menu_options = {
    1: ("Add Credentials", add_credential),
    2: ("View Credentials", view_credential),
    3: ("Quit", request_exit)
}


# Load the vault from disk into the vault_mgr instance.
def load_vault():
    try:
        # Make the vault_mgr global variable writable from local scope.
        global vault_mgr

        # Check if the Vault File exists.
        if not os.path.isfile(vault_file_loc()):
            # Vault path doesn't exist, create it.
            if not os.path.exists(vault_file_loc()):
                os.makedirs(os.path.dirname(vault_file_loc()), exist_ok=True)

            # Logs the vault location to log.txt.
            dump_log(f"Created new vault at '{os.path.realpath(vault_file_loc())}'.")

            # Create a new instance of the Vault Manager class.
            vault_mgr = VaultManager(vault_file_loc())
            vault_mgr.vault_save()

        # Vault does exist
        else:
            vault_mgr = VaultManager.vault_load(vault_file_loc())
    except (MemoryError, EOFError):
        # Delete the Vault
        shutil.rmtree(PATH_VAULT)
        
        # Recreate the Vault
        load_vault()


# Prompt the user with the main menu.
def write_menu():
    print("=============================")
    print("|| DigiCore Password Vault ||")
    print("=============================")
    
    # Iterate over the menu items dictionary
    # to render the menu item titles & index.
    for i in range(1, len(menu_options) + 1):
        menu_title, _ = menu_options[i]
        print(f"|| {i}) {menu_title}")
        
    print()
    user_input = input("|| Enter menu option (number): ")
    print()
    
    return user_input


# Print any unhandled exceptions to the user and prompt contacting supervisor.
def print_error(exception):
    # Allow global variable to be writable from local scope
    global exit_requested
    print("An unexpected error occurred during execution:")
    
    # The formatted error to display.
    error = f"[L{exception.__traceback__.tb_lineno}] [{type(exception).__name__}]: {exception}"
    
    print(error)
    print("Contact your supervisor to report the issue.")
    print(f"Dumping error to '{PATH_LOG}'.")
    
    # Dump the error to the log file.
    dump_log(error)
    
    # Prompt the user to exit and discard the result.
    _ = input("Press <ENTER> to exit.")
    
    # Request exit from the application to prevent data corruption.
    exit_requested = True


# Check for config.ini on disk and load it in, or create it if missing.
def load_config():
    # Make the global variables writable from local scope.
    global config, ROT_CIPHER_SHIFT, PATH_VAULT, PATH_LOG
    
    # Instantiate a ConfigParser instance and store it in config.
    config = configparser.ConfigParser()
    
    # Check if the config already exists, if not create it with default values.
    if not os.path.isfile(PATH_CONFIG):
        config["General"] = {'RotShift': '3', 'VaultPath': './vault', 'LogPath': './log.txt'}
        
        with open(PATH_CONFIG, 'w') as file_config:
            config.write(file_config)
    else:  # Otherwise, read from disk.
        config.read(PATH_CONFIG)
        
    # If there is any issue loading the config values, print the error.
    try:
        ROT_CIPHER_SHIFT = int(config["General"]["RotShift"])
        PATH_VAULT = config["General"]["VaultPath"]
        PATH_LOG = config["General"]["LogPath"]
    except Exception as ex:
        print_error(ex)


# The entry-point of the application,
# where the main execution begins for the application.
def main():
    try:
        # Load the config.ini settings
        load_config()
        
        # Load the user password vault
        load_vault()
    except Exception as ex:
        print_error(ex)
    
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
        except (ValueError, KeyError):  # Ignore value/key errors and re-prompt menu.
            _ = input("Invalid input, enter the correct number next to the menu option.")
        except Exception as ex:  # Unexpected error occurred, log to file.
            print_error(ex)
            
    dump_log("Quit Application")


# If the application is imported as a module,
# this stops any code from running that was intended for direct execution.
if __name__ == "__main__":
    main()
