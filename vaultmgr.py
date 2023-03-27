# This is the VaultEntry class which is used in the VaultManager list.
# It is just a basic data object that stores username, password, and website.
class VaultEntry:
    def __init__(self, username, password, website):
        self.username = username
        self.password = password
        self.website = website


# This is the VaultManager object that holds the vault list and vault related methods.
class VaultManager:
    
    # This acts as a kind of constructor for the class where I can initialize class scope variables.
    def __init__(self):
        self.vault = []

    # This method adds a new entry to the vault.
    def add_entry(self, vault_entry: VaultEntry):
        self.vault.append(vault_entry)

    # This method overwrites any entry in the vault that matches username and website.
    # Replaces the username, password, and website values.
    def overwrite_entry(self, replace_entry: VaultEntry):
        for i in range(len(self.vault)):
            vault_entry = self.vault[i]
            
            if vault_entry.username.lower() == replace_entry.username.lower() and vault_entry.website.lower() == replace_entry.website.lower():
                self.vault[i] = replace_entry
                break
