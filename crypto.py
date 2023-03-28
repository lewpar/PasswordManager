# A class that contains the Rot, Caeser Cipher encrypt and decrypt functions.
# Note: This algorithm is not cryptographically secure, as attackers can brute force
#        the password very easily by shifting it back using the same charset.
# Gist: https://gist.github.com/lewpar/4e63475fb845cdbe9b57385517e09588
class Rot:
    # The charset that defines the shift values.
    CHAR_SET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz`~!@#$%^&*()_-+=|\\}]{[\"':;?/>.<, "

    # Shifts the passphrase by the charset 
    # specified by `shift` places to the right.
    @staticmethod
    def encrypt(passphrase, shift):
        # The list of character that will be joined together later.
        encrypted_chars = []
        
        # Loop over each character in the string passphrase
        for character in passphrase:
            # Get the shifted index from the charset.
            shift_index = Rot.CHAR_SET.find(character) + shift
            
            # Divide the shift_index to wrap back around if the index is too large.
            shift_index = shift_index % len(Rot.CHAR_SET)
            
            # Get the character using the index from the charset.
            shift_char = Rot.CHAR_SET[shift_index]
            
            # Append the character to the list
            encrypted_chars.append(shift_char)
            
        # Join the character together into a single string.
        return "".join(encrypted_chars)

    # Shifts the passphrase by the charset 
    # specified by `shift` places to the left.
    @staticmethod
    def decrypt(passphrase, shift):
        # The list of character that will be joined together later.
        encrypted_chars = []
        
        # Loop over each character in the string passphrase
        for character in passphrase:
            # Get the shifted index from the charset.
            shift_index = Rot.CHAR_SET.find(character) - shift
            
            # Divide the shift_index to wrap back around if the index is too large.
            shift_index = shift_index % len(Rot.CHAR_SET)
            
            # Get the character using the index from the charset.
            shift_char = Rot.CHAR_SET[shift_index]
            
            # Append the character to the list
            encrypted_chars.append(shift_char)
            
        # Join the character together into a single string.
        return "".join(encrypted_chars)
