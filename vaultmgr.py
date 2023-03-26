class VaultEntry:
    def __init__(self, username, password, website):
        self.username = username
        self.password = password
        self.website = website


class VaultManager:
    def __init__(self):
        self.vault = []

    def add_entry(self, vault_entry: VaultEntry):
        self.vault.append(vault_entry)
        
        
    def overwrite_entry(self, replace_entry: VaultEntry):
        for i in range(len(self.vault)):
            vault_entry = self.vault[i]
            
            if vault_entry.username.lower() == replace_entry.username.lower() and vault_entry.website.lower() == replace_entry.website.lower():
                self.vault[i] = replace_entry
                break
