#basic script to generate a ECC keypair using the secp256k1 curve
#compressed format suitable for Bitcoin( after being converted to WIF)
import os
from bitcoin.core import b2x
from bitcoin.wallet import CBitcoinSecret

#Rando key-gen
private_key = CBitcoinSecret.from_secret_bytes(os.urandom(32))

# Output private key(64 bytes) and Public key (33 bytes compressed)
print("Private key (hex):", b2x(private_key)[:64])
print("Public key (compressed, hex):", b2x(private_key.pub))
