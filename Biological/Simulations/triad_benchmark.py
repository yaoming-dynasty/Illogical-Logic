#!/usr/bin/env python3
import hashlib
import itertools
import string
import json

class TopologicalInverseError(Exception):
    """Raised when an inverse bridge operator encounters a non-injective topological collapse."""
    pass

class TriadModeBenchmark:
    def __init__(self, secret_input: str, algo: str, origin_seed: str = "((0/1)))"):
        self.secret_input = secret_input
        self.algo = algo.lower()
        self.origin_seed = origin_seed
        
        h_func = getattr(hashlib, self.algo)
        self.target_hash = h_func(self.secret_input.encode('utf-8')).hexdigest()

    def _hash(self, candidate: str) -> str:
        h_func = getattr(hashlib, self.algo)
        return h_func(candidate.encode('utf-8')).hexdigest()

    def run_normal_mode(self) -> dict:
        """Mode 1: Normal Forward Bridge Triad (B_dec -> B_trans -> B_comp)"""
        print(f"[*] [{self.algo.upper()}] Executing Normal Mode (Forward Entropy Collapse)...")
        forward_hash = self._hash(self.secret_input)
        return {
            "mode": "Normal",
            "status": "COMPLETED",
            "input": self.secret_input,
            "output_hash": forward_hash,
            "description": "Information successfully transformed into public boundary state."
        }

    def run_inverse_mode(self) -> dict:
        """Mode 2: Direct Inverse Bridge Triad (B_dec^(-1) -> B_trans^(-1) -> B_comp^(-1))"""
        print(f"[*] [{self.algo.upper()}] Executing Inverse Mode (Direct Algebraic Inversion)...")
        try:
            # Cryptographic hashes are many-to-one; direct algebraic inverse does not exist.
            raise TopologicalInverseError(
                f"B_trans^(-1) failed for {self.algo.upper()}: Non-injective collapse. "
                "Entropy is irreversibly lost during compression rounds."
            )
        except TopologicalInverseError as e:
            return {
                "mode": "Inverse",
                "status": "TOPOLOGICAL BARRIER ENFORCED",
                "error": str(e),
                "description": "True mathematical inversion is impossible without state-space search."
            }

    def run_inverted_pipeline_mode(self, max_attempts: int = 30000) -> dict:
        """Mode 3: Inverted/Negated Pipeline Loop (B_dec^(-1) -> ¬B_trans -> B_comp^(-1) -> ¬B_dec^(-1) -> Loop)"""
        print(f"[*] [{self.algo.upper()}] Executing Inverted Pipeline Mode (Iterative State Solver)...")
        
        alphabet = string.ascii_letters + string.digits
        iterations = 0
        
        for length in range(1, len(self.secret_input) + 2):
            for candidate_tuple in itertools.product(alphabet, repeat=length):
                candidate = "".join(candidate_tuple)
                iterations += 1
                
                # Pipeline execution stages
                s1 = candidate # B_dec^(-1)
                
                # ¬B_trans (Invert hash bits)
                h_func = getattr(hashlib, self.algo)
                raw_hash = h_func(candidate.encode('utf-8')).digest()
                _ = bytes([b ^ 0xFF for b in raw_hash]) # Negation operator applied
                
                s3 = _ # B_comp^(-1)
                
                # Verification loop ('repeat until solved')
                if self._hash(candidate) == self.target_hash:
                    return {
                        "mode": "Inverted Pipeline",
                        "status": "SOLVED",
                        "iterations": iterations,
                        "recovered_secret": candidate,
                        "verified_hash": self.target_hash
                    }
                    
                if iterations >= max_attempts:
                    break
            if iterations >= max_attempts:
                break

        return {
            "mode": "Inverted Pipeline",
            "status": "TOPOLOGICAL BARRIER ENFORCED",
            "iterations": iterations,
            "description": "Keyspace search budget exhausted before collision resolution."
        }

if __name__ == "__main__":
    test_suite = [
        {"secret": "A", "algo": "md5"},
        {"secret": "XY", "algo": "sha1"},
        {"secret": "Ronio", "algo": "sha256"}
    ]

    comprehensive_results = []
    
    for test in test_suite:
        benchmark = TriadModeBenchmark(secret_input=test["secret"], algo=test["algo"])
        
        res_normal = benchmark.run_normal_mode()
        res_inverse = benchmark.run_inverse_mode()
        res_pipeline = benchmark.run_inverted_pipeline_mode()
        
        comprehensive_results.append({
            "algorithm": test["algo"].upper(),
            "target_secret": test["secret"],
            "modes": [res_normal, res_inverse, res_pipeline]
        })
        print("=" * 60)

    print("\n=== FINAL BENCHMARK SUMMARY REPORT ===")
    print(json.dumps(comprehensive_results, indent=4))
