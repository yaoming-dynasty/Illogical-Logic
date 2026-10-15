#!/usr/bin/env python3
"""Protein boundary folding simulator

This module provides a tiny, rule-based folding simulator and a CLI so it can
be run directly as a script:

    python Biological/Simulations/Protein_Folding_Simulation.py -s HHPPHLHPHHPP

The CLI accepts an explicit sequence, or can generate a random sequence.
Allowed residue characters: H (hydrophobic), P (polar), L (interface).
"""

import argparse
import json
import random
import sys
from typing import List


class ProteinBoundaryFoldingSimulator:
    def __init__(self, sequence: str, origin_seed: str = "((0/1)))"):
        self.origin_seed = origin_seed
        # Primary sequence where 'H' = Hydrophobic (Inside seeker) and 'P' = Polar (Outside seeker)
        self.sequence = list(sequence)

    def fold_simulation(self) -> dict:
        """
        Simulates the Transformation Bridge (B_trans):
        Linear sequence transforms into a spatial boundary configuration 
        where hydrophobic residues migrate to {The_Boundary_Inside}.
        """
        inside_core: List[str] = []
        outside_solvent: List[str] = []
        boundary_interface: List[str] = []

        # Step 1: Evaluate relative affinities based on residue type
        for idx, residue in enumerate(self.sequence):
            # The relational operator '~' maps each residue relative to the solvent environment
            if residue == 'H':
                # Hydrophobic seeks {The_Boundary_Inside}
                inside_core.append(f"Residue_{idx}(H)")
            elif residue == 'P':
                # Polar seeks {The_Outside_Boundary}
                outside_solvent.append(f"Residue_{idx}(P)")
            else:
                # Amphipathic acts as {The_Boundary_LIne}
                boundary_interface.append(f"Residue_{idx}(L)")

        # Step 2: Compute structural stability score via boundary segregation
        folding_efficiency = len(inside_core) / (len(self.sequence) + 1e-9)

        simulation_receipt = {
            "framework_axiom": "((0/1))) ~ {The_Boundary_Inside} + {The_Outside_Boundary} + {The_Boundary_LIne}",
            "bridge_operator": "B_trans(Linear Chain -> 3D Native State)",
            "origin_seed": self.origin_seed,
            "primary_sequence": "".join(self.sequence),
            "topological_state": {
                "{The_Boundary_Inside} (Hydrophobic Core)": inside_core,
                "{The_Boundary_LIne} (Interface / Backbone)": boundary_interface,
                "{The_Outside_Boundary} (Aqueous Solvent)": outside_solvent,
            },
            "folding_stability_index": round(folding_efficiency, 3),
            "status": "FOLDED_AND_STABILIZED",
        }
        return simulation_receipt


def _validate_sequence(seq: str) -> str:
    """Validate and normalise a sequence string.

    Allowed characters are H, P, and L. Any lowercase letters are accepted and
    converted to uppercase. If other characters are present, the function will
    raise a ValueError.
    """
    if not seq:
        raise ValueError("Sequence must not be empty")
    seq_up = seq.upper()
    allowed = set("HPL")
    invalid = sorted({c for c in seq_up if c not in allowed})
    if invalid:
        raise ValueError(f"Invalid residue characters in sequence: {''.join(invalid)}. Allowed: H, P, L")
    return seq_up


def _random_sequence(length: int) -> str:
    choices = ["H", "P", "L"]
    return "".join(random.choice(choices) for _ in range(length))


def main(argv=None):
    parser = argparse.ArgumentParser(description="Run the ProteinBoundaryFoldingSimulator on a short sequence")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-s", "--sequence", type=str, help="Residue sequence (e.g. HHPPHLHP)")
    group.add_argument("-r", "--random", type=int, metavar="N", help="Generate a random sequence of length N")
    parser.add_argument("--origin-seed", type=str, default="((0/1)))", help="Origin seed string to include in the output")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON output")

    args = parser.parse_args(argv)

    try:
        if args.sequence:
            seq = _validate_sequence(args.sequence)
        else:
            if args.random <= 0:
                raise ValueError("Random sequence length must be > 0")
            seq = _random_sequence(args.random)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2

    simulator = ProteinBoundaryFoldingSimulator(sequence=seq, origin_seed=args.origin_seed)
    result = simulator.fold_simulation()

    if args.pretty:
        print(json.dumps(result, indent=4))
    else:
        print(json.dumps(result))

    return 0


if __name__ == "__main__":
    # When invoked directly, run the CLI main() function. Exit code is propagated.
    raise SystemExit(main())
