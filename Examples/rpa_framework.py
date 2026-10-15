#!/usr/bin/env python3
import argparse
import hashlib
import json
import secrets
import sys
import os
import requests

# Optional dependency: web3
try:
    from web3 import Web3
except Exception:
    Web3 = None

class RelationalBoundaryFramework:
    def __init__(self, author: str, origin_seed: str = "((0/1)))"):
        self.origin_seed = origin_seed
        self.author = author
        # {The_Boundary_Inside}: Private entropy unique to the author
        # _inside_private_salt may be overridden for deterministic receipts
        self._inside_private_salt = secrets.token_hex(16)
        
    def seal_authorship(self, framework_spec: str) -> dict:
        """
        Applies the relational operator '~' to map the origin, 
        internal author state, and framework text across the boundary line.
        """
        inside_state = f"AUTHOR:{self.author}|SALT:{self._inside_private_salt}"
        
        # {The_Boundary_LIne}: The cryptographic hashing function acting as the interface
        boundary_line_input = f"{self.origin_seed} ~ ({inside_state}) ~ [{framework_spec}]"
        
        # {The_Outside_Boundary}: The public ledger digest
        outside_digest = hashlib.sha256(boundary_line_input.encode('utf-8')).hexdigest()
        
        commitment_receipt = {
            "framework_axiom": "((0/1))) ~ {The_Boundary_Inside} + {The_Outside_Boundary} + {The_Boundary_LIne}",
            "certified_author": self.author,
            "origin_seed": self.origin_seed,
            "public_digest_commitment": outside_digest,
            "status": "SEALED_AND_VERIFIED"
        }
        return commitment_receipt


def upload_to_pinata(json_obj, jwt_token):
    """Pin JSON to Pinata using JWT. Returns CID on success."""
    url = "https://api.pinata.cloud/pinning/pinJSONToIPFS"
    headers = {
        'Authorization': f'Bearer {jwt_token}',
        'Content-Type': 'application/json'
    }
    response = requests.post(url, headers=headers, json={"pinataContent": json_obj})
    if response.status_code == 200:
        return response.json().get('IpfsHash')
    else:
        raise RuntimeError(f"Pinata error: {response.status_code} {response.text}")


def upload_to_local_ipfs(json_bytes, api_url='http://127.0.0.1:5001/api/v0/add'):
    """Upload raw bytes to a local IPFS daemon's HTTP API. Returns CID."""
    files = {'file': ('receipt.json', json_bytes)}
    response = requests.post(api_url, files=files)
    if response.status_code in (200, 201):
        try:
            j = response.json()
        except Exception:
            # ipfs add might return plain text with JSON per line; try to parse first line
            j = json.loads(response.text.splitlines()[-1])
        return j.get('Hash')
    else:
        raise RuntimeError(f"IPFS API error: {response.status_code} {response.text}")


def anchor_cid_on_ethereum(cid, rpc_url, private_key, chain_id=None):
    """Create a simple transaction that includes the CID in the data field and broadcast it.
    Returns the transaction hash.
    NOTE: This will broadcast a real transaction and spend funds. Use with care.
    """
    if Web3 is None:
        raise RuntimeError('web3.py is required for anchoring to Ethereum. Install with `pip install web3`')

    w3 = Web3(Web3.HTTPProvider(rpc_url))
    if not w3.isConnected():
        raise RuntimeError('Could not connect to RPC URL')

    account = w3.eth.account.from_key(private_key)
    from_addr = account.address

    # Prepare transaction payload: place the CID as utf-8 bytes in data
    data_bytes = cid.encode('utf-8')
    data_hex = '0x' + data_bytes.hex()

    nonce = w3.eth.get_transaction_count(from_addr)

    # Basic tx dict
    tx = {
        'nonce': nonce,
        'to': None,  # contract creation / or empty to send to burn; leave None to allow data-only
        'value': 0,
        'data': data_hex,
        'gasPrice': w3.eth.gas_price,
    }

    # Estimate gas - many providers require a 'to' address; estimate with a simple call
    try:
        gas_estimate = w3.eth.estimate_gas({
            'from': from_addr,
            'to': tx['to'],
            'value': tx['value'],
            'data': tx['data']
        })
    except Exception:
        # fallback to a conservative default
        gas_estimate = 200_000

    tx['gas'] = int(gas_estimate * 1.2)

    if chain_id is None:
        try:
            chain_id = w3.eth.chain_id
        except Exception:
            chain_id = 1
    tx['chainId'] = chain_id

    signed = w3.eth.account.sign_transaction(tx, private_key=private_key)

    tx_hash = w3.eth.send_raw_transaction(signed.rawTransaction)
    return tx_hash.hex()


def main(argv=None):
    parser = argparse.ArgumentParser(description='Relational Proof of Authorship (RPA) with IPFS anchoring')
    parser.add_argument('--file', '-f', help='Optional input file (e.g., Algebraic.md) to include in the commitment')
    parser.add_argument('--seed', '-s', help='Optional seed to derive a deterministic private salt')
    parser.add_argument('--author', '-a', default='Christopher Thomas Ronio', help='Author name to certify')
    parser.add_argument('--ipfs', action='store_true', help='Upload the receipt JSON to IPFS')
    parser.add_argument('--pinata_jwt', help='Pinata JWT for pinning to Pinata (optional)')
    parser.add_argument('--ipfs_api_url', help='Alternative IPFS API URL (e.g., http://127.0.0.1:5001/api/v0/add)')
    parser.add_argument('--anchor', action='store_true', help='Anchor the resulting CID on a blockchain (Ethereum-compatible)')
    parser.add_argument('--rpc_url', help='RPC URL for the target blockchain (required for anchoring)')
    parser.add_argument('--private_key_env', default='ANCHOR_PRIVATE_KEY', help='Environment variable name containing the private key')
    parser.add_argument('--chain_id', type=int, help='Optional chain id to use for anchoring transaction')
    args = parser.parse_args(argv)

    # Core spec fallback
    core_spec = "A mathematical framework for relational boundaries, nested topology, and sovereign identity."

    # Read file content if provided
    if args.file:
        try:
            with open(args.file, 'r', encoding='utf-8') as fh:
                core_spec = fh.read()
        except Exception as e:
            print(json.dumps({"error": f"Could not read file {args.file}: {e}"}))
            sys.exit(1)

    # Initialize framework for the specified author
    rpa = RelationalBoundaryFramework(author=args.author)

    # If a seed is provided, derive a deterministic salt so the receipt is reproducible
    if args.seed:
        # take a digest of the seed to produce a deterministic salt length similar to token_hex(16)
        derived = hashlib.sha256(args.seed.encode('utf-8')).hexdigest()[:32]
        rpa._inside_private_salt = derived

    receipt = rpa.seal_authorship(core_spec)

    receipt_json = json.dumps(receipt, indent=4)
    print(receipt_json)

    cid = None
    if args.ipfs:
        # Prepare bytes
        json_bytes = receipt_json.encode('utf-8')
        try:
            if args.pinata_jwt:
                print('[*] Uploading receipt to Pinata...')
                cid = upload_to_pinata(receipt, args.pinata_jwt)
            else:
                api_url = args.ipfs_api_url or os.environ.get('IPFS_API_URL') or 'http://127.0.0.1:5001/api/v0/add'
                print(f'[*] Uploading receipt to IPFS API at {api_url}...')
                cid = upload_to_local_ipfs(json_bytes, api_url=api_url)
            print(f'[*] IPFS CID: {cid}')
        except Exception as e:
            print(json.dumps({"error": f"IPFS upload failed: {e}"}))
            sys.exit(1)

    if args.anchor:
        if not cid:
            print(json.dumps({"error": "Anchoring requested but no CID available. Use --ipfs to upload first."}))
            sys.exit(1)
        rpc = args.rpc_url or os.environ.get('ANCHOR_RPC_URL')
        priv_env = args.private_key_env or 'ANCHOR_PRIVATE_KEY'
        priv = os.environ.get(priv_env)
        if not rpc or not priv:
            print(json.dumps({"error": "Anchoring requires an RPC URL (via --rpc_url or ANCHOR_RPC_URL env) and a private key in the environment."}))
            sys.exit(1)
        try:
            print('[*] Anchoring CID on the blockchain...')
            tx_hash = anchor_cid_on_ethereum(cid, rpc, priv, chain_id=args.chain_id)
            print(f'[*] Anchor transaction sent: {tx_hash}')
        except Exception as e:
            print(json.dumps({"error": f"Anchoring failed: {e}"}))
            sys.exit(1)


if __name__ == "__main__":
    main()
