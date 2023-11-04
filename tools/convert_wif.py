from bitcoin.wallet import CBitcoinSecret
from bitcoin.core import b2x
import bitcoin

def private_key_to_wif(hex_private_key):
    private_key_bytes = bytes.fromhex(hex_private_key)
    # For testnet
    bitcoin.SelectParams('testnet')
    # Construct a CBitcoinSecret object
    private_key = CBitcoinSecret.from_secret_bytes(private_key_bytes)
    # Convert to Wallet Import Format (WIF)
    wif_private_key = str(private_key)
    return wif_private_key

#  Add your hex private key
hex_private_key = ""

print("Hex Private Key:", hex_private_key)
print("Testnet WIF Private Key:", private_key_to_wif(hex_private_key))

