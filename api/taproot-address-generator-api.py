# A basic API I setup to create tweaked public keys and derived taproot addresses with time lock and preimage conditions.
# Hope it's useful to someone 

from flask import Flask, request, jsonify
import hashlib
from coincurve import PublicKey
from bech32 import bech32_encode, convertbits

app = Flask(__name__)

# Tweak the orignal Pub key
def tweak_pubkey(original_pubkey_hex, tweak_bytes):
    original_pubkey_bytes = bytes.fromhex(original_pubkey_hex)
    pubkey = PublicKey(original_pubkey_bytes)
    tweaked_pubkey = pubkey.add(tweak_bytes)
    return tweaked_pubkey.format().hex()

# Derive the Bitcoin Taproot address from the Pub key
def create_p2tr_address(tweaked_pubkey_hex, timelock=None, preimage=None):
    tweaked_pubkey_bytes = bytes.fromhex(tweaked_pubkey_hex)
    program = hashlib.sha256(tweaked_pubkey_bytes).digest()

    # Tapleaf timelock script
    if timelock:
        # Example CSV script: "<timelock> OP_CSV OP_DROP"
        timelock_script = bytes([timelock & 0xFF, (timelock >> 8) & 0xFF]) + b'\xB2\x75'  # B2 = OP_CSV, 75 = OP_DROP
        program = hashlib.sha256(timelock_script + program).digest()

    # A preimage condition 
    if preimage:
        # Example preimage script: "OP_HASH160 <hash160(preimage)> OP_EQUAL"
        hash160_preimage = hashlib.new('ripemd160', hashlib.sha256(bytes.fromhex(preimage)).digest()).digest()
        preimage_script = b'\xA9\x14' + hash160_preimage + b'\x87'  # A9 = OP_HASH160, 14 = push 20 bytes, 87 = OP_EQUAL
        program = hashlib.sha256(preimage_script + program).digest()

    # Assemble the address
    data = [0x01] + convertbits(program, 8, 5)
    address = bech32_encode('tb', data)

    return address

# Create proof enpoint, generates tweaked public key and a Taproot address for a given orignal public key, and message(the answer to the preimage) and a timelock
@app.route('/createproof', methods=['POST'])
def create_proof():
    data = request.json
    message = data['message']
    original_pubkey_hex = data['original_pubkey_hex']
    timelock = data.get('timelock', None)
    preimage = data.get('preimage', None)

    tweak_bytes = hashlib.sha256(message.encode()).digest()
    tweaked_pubkey_hex = tweak_pubkey(original_pubkey_hex, tweak_bytes)
    address = create_p2tr_address(tweaked_pubkey_hex, timelock, preimage)

    return jsonify({"address": address, "tweaked_pubkey": tweaked_pubkey_hex, "timelock": timelock, "preimage": preimage})


# To test, although like hashing... rerunning proof endpoint is effectively the same 
@app.route('/verifyproof', methods=['POST'])
def verify_proof():
    data = request.json
    message = data['message']
    original_pubkey_hex = data['original_pubkey_hex']
    tweaked_pubkey_hex = data['tweaked_pubkey_hex']
    timelock = data.get('timelock', None)
    preimage = data.get('preimage', None)

    tweak_bytes = hashlib.sha256(message.encode()).digest()
    expected_tweaked_pubkey_hex = tweak_pubkey(original_pubkey_hex, tweak_bytes)

    if expected_tweaked_pubkey_hex == tweaked_pubkey_hex:
        return jsonify({"result": "success", "message": "The proof is valid"})
    else:
        return jsonify({"result": "error", "message": "The proof is invalid"}), 400


# runs on default 5000 as per normal flask apps, can be changed here
if __name__ == '__main__':
    app.run(debug=True)
