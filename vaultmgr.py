# Imports the serialization tools, otherwise known as 'pickling'.
# This allows me to write class objects to disk.
import pickle

# This is the VaultEntry class which is used in the VaultManager list.
# It is just a basic data object that stores username, password, and resource.
class VaultEntry:
    def __init__(self, username, password, resource):
        self.username = username
        self.password = password
        self.resource = resource


# This is the VaultManager object that holds the vault list and vault related methods.
class VaultManager:
    
    # This acts as a kind of constructor for the class where I can initialize class scope variables.
    def __init__(self, path_vault):
        self.vault = []
        self.path_vault = path_vault

    # This method adds a new entry to the vault.
    def add_entry(self, vault_entry: VaultEntry):
        self.vault.append(vault_entry)

    # This method overwrites any entry in the vault that matches username and resource.
    # Replaces the username, password, and resource values.
    def overwrite_entry(self, replace_entry: VaultEntry):
        for i in range(len(self.vault)):
            vault_entry = self.vault[i]
            
            if vault_entry.username.lower() == replace_entry.username.lower() and vault_entry.resource.lower() == replace_entry.resource.lower():
                self.vault[i] = replace_entry
                break
            
    # Saves the vault to disk by serializing the vault list to bytes.
    def vault_save(self):
        # Write a new VaultManager file to disk. Using mode 'wb' -> 'write', 'binary'
        with open(self.path_vault, "wb") as vault_file:
            # Serialize the VaultManager to a byte array.
            pickle.dump(self, vault_file)
    
    # Loads the vault from disk, deserializing to a VaultManager instance.
    @staticmethod
    def vault_load(path_vault):
        # Read the vault file from disk. Using mode 'rb' -> 'read', 'binary'
        with open(path_vault, "rb") as vault_file:
            # Deserialize the vault file back into an instance of
            # VaultManager.
            return pickle.load(vault_file)
