# Bitcoin Taproot Address API

This repository contains a Flask-based API that allows users to generate and verify Bitcoin Taproot addresses with optional spending conditions such as timelocks and hash preimages. It serves as an educational and practical tool for understanding the intricacies of Taproot and Bech32m encoding. Central to this whole process is "Key Tweaking"

## Features

- **Key Tweaking:** Generate tweaked public keys based on original public keys and tweak values.
- **Taproot Address Generation:** Create Pay-to-Taproot (P2TR) addresses from tweaked public keys.
- **Spending Conditions:** Optionally include timelocks and hash preimage conditions in the Taproot address.
- **Bech32m Encoding:** Custom implementation of Bech32m encoding for generating Taproot addresses.
- **Verification:** Verify the validity of a proof created using the API.

## How to Use

### Setup

Clone the repository and install the required dependencies:

    git clone https://github.com/your-username/taproot-address-api.git
    cd taproot-address-api
    pip install -r requirements.txt

### Running the API

Start the Flask app:

    python app.py

The API will be accessible at `http://127.0.0.1:5000/`.

## API Endpoints

- **Create Proof** (`/createproof`): Generates a Taproot address with optional spending conditions.
    - **POST Parameters:** `message`, `original_pubkey_hex`, `timelock` (optional), `preimage` (optional)
    - **Response:** Taproot address, tweaked public key, timelock, preimage

- **Verify Proof** (`/verifyproof`): Verifies the validity of a proof.
    - **POST Parameters:** `message`, `original_pubkey_hex`, `tweaked_pubkey_hex`, `timelock` (optional), `preimage` (optional)
    - **Response:** Verification result

## Examples

### Example 1: Create Proof

**Request:**

    POST /createproof
    {
        "message": "Hello, Taproot!",
        "original_pubkey_hex": "03b0c5916e1e5a3c4c8e0f4e165a4a267e0152782c5a315a232c367d0d1f1c598"
    }

**Response:**

    {
        "address": "tb1p7tu4n5yv8l2hfy2sgxwpuce2gku4a8eacp483k4h5r7c9w9lpk7sg2tqzq",
        "tweaked_pubkey": "02c2662c97488c917011e6f3c018e449f8e67f5e5a7d5ed7be6e0fcee559781b2e",
        "timelock": null,
        "preimage": null
    }

### Example 2: Create Proof with Timelock and Preimage

**Request:**

    POST /createproof
    {
        "message": "Secure Message",
        "original_pubkey_hex": "03b0c5916e1e5a3c4c8e0f4e165a4a267e0152782c5a315a232c367d0d1f1c598",
        "timelock": 10,
        "preimage": "68656c6c6f20776f726c64"  # ASCII for "hello world" in hex
    }

**Response:**

    {
        "address": "tb1p3x7yjz0x7z2c5jsnvs6fu8ur0sq6n6hkp3m3f3vrj7qw0crx7x9sw7cgk5",
        "tweaked_pubkey": "03e8e8f9f32f1e20cf7f9e1b16d9cc7a68f0b6a5860e6e7504b50e2e0f3cd437c",
        "timelock": 10,
        "preimage": "68656c6c6f20776f726c64"
    }

### Example 3: Verify Proof

**Request:**

    POST /verifyproof
    {
        "message": "Hello, Taproot!",
        "original_pubkey_hex": "03b0c5916e1e5a3c4c8e0f4e165a4a267e0152782c5a315a232c367d0d1f1c598",
        "tweaked_pubkey_hex": "02c2662c97488c917011e6f3c018e449f8e67f5e5a7d5ed7be6e0fcee559781b2e"
    }

**Response:**

    {
        "result": "success",
        "message": "The proof is valid"
    }

## Contributing

Feel free to fork this repo, add comments, and I hope it helps you to explore more about what Taproot can do. :)

## License

This project is licensed under the MIT License. See the `LICENSE.md` file for details.
