__author__ = 'karon'

# TODO: change hmac_key to be imported via params of functions

from Crypto.Cipher import AES
from hashlib import sha256
import hmac
import os

aes_blocksize = 16  # This is the default AES blocksize and can't be changed
mac_size = 32  # This is the default size for the SHA256 hash


def encrypt(hmac_key, aes_key, plaintext):
    # Create a 32 byte hashstring with the provided key
    hashkey = sha256(aes_key).digest()

    # Create a random Initialization Vector with the size of the AES blocksize
    iv = os.urandom(aes_blocksize)

    # Create a cipher which uses the Cipher-Block Chaining mode
    cipher = AES.new(hashkey, AES.MODE_CBC, iv)

    # Create the ciphertext based on the padded plaintext and calculated with the hashed key and random IV
    ciphertext = cipher.encrypt(_pad(plaintext))

    # Sign the ciphertext with a Hashed MAC to ensure data integrity and authentication when decrypting it.
    # This is done according to the "encrypt-then-mac" principle.
    # This basically prevents attacks like the "Padding Oracle Attack".
    mac = hmac.new(hmac_key, iv + ciphertext, sha256).digest()

    # Return the full ciphertext (IV followed by ciphertext followed by the HMAC)
    # This is encoded with base64 so it can be saved on the database
    return (iv + ciphertext + mac).encode("base64")


def decrypt(hmac_key, aes_key, ciphertext):
    # First decode the password back to binary format
    ciphertext = ciphertext.decode("base64")

    # Get the Hashed mac out of the ciphertext
    mac = ciphertext[-mac_size:]

    # Check if the new calculated Hashed MAC is still the same as the provided one.
    # So we can be sure that the cipher data isn't changed.
    # FUTURE: Change this if statement to use the compare_digest() function!!
    #         -> This to counter timing attacks, this is available in python version 2.7.7
    #         -> https://docs.python.org/2/library/hmac.html
    if mac == hmac.new(hmac_key, ciphertext[:-mac_size], sha256).digest():
        # Create a 32 byte hashstring with the provided key
        hashkey = sha256(aes_key).digest()

        # Get the IV out of the first 16 bytes of the ciphertext (IV is same size as AES blocksize)
        iv = ciphertext[:aes_blocksize]
        # Get the actual ciphertext seperated from the IV and MAC
        ciphertext = ciphertext[aes_blocksize:-mac_size]

        # Create a new cipherbox which uses the Cipher-Block chaining mode
        cipher = AES.new(hashkey, AES.MODE_CBC, iv)

        # Decrypt the ciphertext
        plaintext = cipher.decrypt(ciphertext)

        # Return the ciphertext without the padding
        return _unpad(plaintext)
    else:
        return 1


def _pad(plaintext):
    # Padding with PKCS#7 (blocksizes supported: < 256)
    # Determing the number of bytes to pad: between 1 and 16
    length = aes_blocksize - (len(plaintext) % aes_blocksize)
    # Create a pad of characters all representing the N bytes of pad length
    pad = chr(length)*length

    # Retugn the plaintext together with the pad
    return plaintext + pad


def _unpad(plaintext):
    # Take last byte of text and convert it to the length integer
    padlength = ord(plaintext[len(plaintext)-1:])

    #Remove padding of plaintext
    plaintext = plaintext[:-padlength]

    # Return the plaintext without the padding
    return plaintext


if __name__ == '__main__':
    enc = encrypt("qdsfi5465****5654ttCDd$$$$%%74", "tsdfsdfsdest", "*tgfr8745*")
    print enc
    print decrypt("qdsfi5465****5654ttCDd$$$$%%74", "tsdfsdfsdest", enc)