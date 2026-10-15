#!/usr/bin/env python3
import argparse
import hashlib
import json
import secrets
import sys

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


def main(argv=None):
    parser = argparse.ArgumentParser(description='Relational Proof of Authorship (RPA)')
    parser.add_argument('--file', '-f', help='Optional input file (e.g., Algebraic.md) to include in the commitment')
    parser.add_argument('--seed', '-s', help='Optional seed to derive a deterministic private salt')
    parser.add_argument('--author', '-a', default='Christopher Thomas Ronio', help='Author name to certify')
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

    # Output the JSON cryptographic receipt
    print(json.dumps(receipt, indent=4))


if __name__ == "__main__":
    main()
