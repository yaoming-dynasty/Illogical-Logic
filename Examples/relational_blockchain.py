#!/usr/bin/env python3
"""
Module: relational_blockchain.py
Framework: Relational Boundary Framework (((0/1))) ~ {The_Boundary_Inside} + {The_Outside_Boundary} + {The_Boundary_LIne}
Author: Christopher Thomas Ronio
Description: Implements a topological blockchain ledger where blocks are bounded, 
                 nested containers verified via the Bridge Triad and iterative boundary solvers.
"""

import hashlib
import json
import time

class TopologicalBlockViolation(Exception):
    """Raised when a block or transaction breaches structural boundary invariants."""
    pass

class RelationalBlock:
    def __init__(self, index: int, transactions: list, previous_hash: str, origin_seed: str = "((0/1)))"):
        self.index = index
        self.timestamp = time.time()
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.origin_seed = origin_seed
        self.nonce = 0
        self.hash = self.compute_boundary_hash()

    def compute_boundary_hash(self) -> str:
        """
        Computes the block's cryptographic boundary hash using the B_trans operator pipeline.
        """
        block_data = {
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": self.transactions,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce,
            "axiom": self.origin_seed
        }
        encoded_block = json.dumps(block_data, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def mine_block(self, difficulty: int):
        """
        Iterative state-space solver loop ('repeat the hash until solved') 
        enforcing the boundary difficulty target.
        """
        target = "0" * difficulty
        print(f"[*] Mining Block {self.index} through Topological Boundary Solver...")
        while not self.hash.startswith(target):
            self.nonce += 1
            self.hash = self.compute_boundary_hash()
        print(f"[+] Block {self.index} Solved! Nonce: {self.nonce} | Hash: {self.hash[:16]}...")

class RelationalBlockchain:
    def __init__(self, difficulty: int = 2):
        self.chain = []
        self.difficulty = difficulty
        self.origin_seed = "((0/1)))"
        self.create_genesis_block()

    def create_genesis_block(self):
        """Initializes the origin boundary seed block."""
        genesis_block = RelationalBlock(
            index=0, 
            transactions=[{"sender": "SYSTEM", "receiver": "ROOT", "amount": 0.0, "note": "Origin Seed ((0/1)))"}], 
            previous_hash="0", 
            origin_seed=self.origin_seed
        )
        self.chain.append(genesis_block)

    def get_latest_block(self) -> RelationalBlock:
        return self.chain[-1]

    def _decompose_and_validate_transactions(self, transactions: list) -> list:
        """
        Step 1: B_dec (Decomposition) - Evaluates transaction invariants 
        inside {The_Boundary_Inside} before block composition.
        """
        valid = []
        for tx in transactions:
            if not all(k in tx for k in ("sender", "receiver", "amount")):
                raise TopologicalBlockViolation("Transaction structure invalid: Missing required boundary keys.")
            if tx["amount"] < 0:
                raise TopologicalBlockViolation("Topological Singularity: Negative transaction amount detected.")
            valid.append(tx)
        return valid

    def add_block(self, transactions: list):
        """
        Applies the Bridge Triad (B_dec -> B_trans -> B_comp) to validate, 
        mine, and append a new block across the boundary line.
        """
        # Step 1: Decomposition & Validation
        validated_txs = self._decompose_and_validate_transactions(transactions)
        
        # Step 2: Transformation & Composition into a new block
        previous_block = self.get_latest_block()
        new_block = RelationalBlock(
            index=len(self.chain),
            transactions=validated_txs,
            previous_hash=previous_block.hash,
            origin_seed=self.origin_seed
        )
        
        # Execute iterative boundary solver loop
        new_block.mine_block(self.difficulty)
        
        # Append to immutable ledger chain
        self.chain.append(new_block)
        print(f"[+] Block successfully composed and added to the Relational Ledger.\n")

    def verify_chain_integrity(self) -> bool:
        """Verifies that no container level-collapse or hash tampering has occurred."""
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i-1]

            if current.hash != current.compute_boundary_hash():
                print(f"[-] Integrity Failure: Block {i} hash mismatch.")
                return False
            
            if current.previous_hash != previous.hash:
                print(f"[-] Integrity Failure: Block {i} severed from previous boundary line.")
                return False
        
        print("[*] Chain Topological Integrity Verified: All boundary walls secure.")
        return True

if __name__ == "__main__":
    print(f"=== RELATIONAL BOUNDARY FRAMEWORK: TOPOLOGICAL BLOCKCHAIN ===")
    print(f"Framework Axiom: ((0/1))) ~ {{The_Boundary_Inside}} + {{The_Outside_Boundary}} + {{The_Boundary_LIne}}\n")

    ledger = RelationalBlockchain(difficulty=2)

    # Add blocks through the framework pipeline
    ledger.add_block([
        {"sender": "Christopher Ronio", "receiver": "Node_Alpha", "amount": 50.0, "note": "Initial framework allocation"}
    ])
    
    ledger.add_block([
        {"sender": "Node_Alpha", "receiver": "Node_Beta", "amount": 12.5, "note": "Topological transition transfer"}
    ])

    # Verify immutable chain integrity
    ledger.verify_chain_integrity()
    
    # Print ledger summary
    ledger_summary = [
        {"index": b.index, "hash": b.hash[:16], "prev_hash": b.previous_hash[:16], "tx_count": len(b.transactions)} 
        for b in ledger.chain
    ]
    print("\n--- LEDGER SUMMARY MANIFEST ---")
    print(json.dumps(ledger_summary, indent=4))
