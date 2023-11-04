#
#A simple setup to take your original private key, the tweak as per your 'message' and generate the corresponding 'tweaked private key' 
#
#
from coincurve import PrivateKey
import hashlib

def tweak_private_key(original_private_key_hex, message):
    # Ensure the private key is 64 characters long (32 bytes)
    if len(original_private_key_hex) != 64:
        raise ValueError("Private key must be 64 characters long (32 bytes).")

    # Convert the hex private key to a PrivateKey object
    original_private_key_bytes = bytes.fromhex(original_private_key_hex)
    original_private_key = PrivateKey(original_private_key_bytes)

    # Hash the message to create the tweak
    tweak_bytes = hashlib.sha256(message.encode()).digest()
    tweak_int = int.from_bytes(tweak_bytes, byteorder='big')

    # Curve order for secp256k1
    CURVE_ORDER = 115792089237316195423570985008687907852837564279074904382605163141518161494337

    # Compute the tweaked private key
    tweaked_private_key_int = (original_private_key.to_int() + tweak_int) % CURVE_ORDER
    tweaked_private_key_bytes = tweaked_private_key_int.to_bytes(32, byteorder='big')
    tweaked_private_key_hex = tweaked_private_key_bytes.hex()

    print("Original private key (hex):", original_private_key_hex)
    print("Tweaked private key (hex):", tweaked_private_key_hex)


original_private_key_hex = ""
message = "Hello, World!"
tweak_private_key(original_private_key_hex, message)

