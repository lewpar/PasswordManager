class VaultEntry:
    def __init__(self, username, password, address):
        self.username = username
        self.password = password
        self.address = address


class VaultManager:
    def __init__(self):
        self.vault = []

    def add_entry(self, vault_entry: VaultEntry):
        self.vault.append(vault_entry)
