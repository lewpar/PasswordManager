# A class that contains the Rot, Caeser Cipher encrypt and decrypt functions.
# Gist: https://gist.github.com/lewpar/4e63475fb845cdbe9b57385517e09588
class Rot:
    # The charset that defines the shift values.
    CHAR_SET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz`~!@#$%^&*()_-+=|\}]{[\"':;?/>.<, "

    # Shifts the passphrase by the charset 
    # specified by `shift` places to the right.
    @staticmethod
    def encrypt(passphrase, shift):
        # Using list comprehension to transform the passphrase into the shifted passphrase,
        # stored as a list of characters.
        encrypted_phrase = [Rot.CHAR_SET[(Rot.CHAR_SET.find(c) + shift) % len(Rot.CHAR_SET)] for c in passphrase]
        
        # Join the characters together, into a string.
        return "".join(encrypted_phrase)

    # Shifts the passphrase by the charset 
    # specified by `shift` places to the left.
    @staticmethod
    def decrypt(passphrase, shift):
        # Using list comprehension to transform the shifted passphrase into the un-shifted passphrase,
        # stored as a list of characters.
        decrypted_phrase = [Rot.CHAR_SET[(Rot.CHAR_SET.find(c) - shift) % len(Rot.CHAR_SET)] for c in passphrase]
        
        # Join the characters together, into a string.
        return "".join(decrypted_phrase)