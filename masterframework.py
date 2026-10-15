```python
"""
RELATIONAL BOUNDARY FRAMEWORK
Logic-Gate Computational Model

Author:
    Christopher Thomas Ronio

Core relationship:

    {Many & Few}
        =
    {Boundary Inside}
        +
    {Outside Boundary}
        +
    {Boundary Line}

Computational interpretation:

    X = input state
    T(X) = logic-gate transformation
    F(X) = boundary classification

For Boolean systems:

    X = (A, B)
    T(X) = Gate(A, B)
    Y = {0, 1}

    Y = 1  -> INSIDE
    Y = 0  -> OUTSIDE

The logic gate itself is the BOUNDARY LINE.
"""


from dataclasses import dataclass
from typing import Callable


# =============================================================
# BOOLEAN BOUNDARY STATE
# =============================================================

@dataclass(frozen=True)
class BooleanState:
    A: int
    B: int

    def __post_init__(self):
        if self.A not in (0, 1):
            raise ValueError("A must be 0 or 1")

        if self.B not in (0, 1):
            raise ValueError("B must be 0 or 1")


# =============================================================
# RELATIONAL BOUNDARY GATE
# =============================================================

class BoundaryLogicGate:

    def __init__(
        self,
        name: str,
        gate: Callable[[int, int], int]
    ):
        self.name = name
        self.gate = gate

    # ---------------------------------------------------------
    # T(X)
    # ---------------------------------------------------------

    def transform(self, state: BooleanState) -> int:
        """
        T(X)

        Transforms the input boundary state into
        a Boolean output.
        """

        return self.gate(state.A, state.B)

    # ---------------------------------------------------------
    # BOUNDARY CLASSIFICATION
    # ---------------------------------------------------------

    def classify(self, state: BooleanState) -> dict:

        output = self.transform(state)

        if output == 1:

            boundary = "INSIDE"

        else:

            boundary = "OUTSIDE"

        return {
            "input": (state.A, state.B),
            "output": output,
            "boundary": boundary,
            "gate": self.name
        }

    # ---------------------------------------------------------
    # MANY & FEW
    # ---------------------------------------------------------

    def many_few(self, state: BooleanState) -> dict:

        output = self.transform(state)

        if output == 1:

            return {
                "many_few": "FEW -> INSIDE",
                "meaning":
                    "The input combination satisfies the boundary."
            }

        return {
            "many_few": "MANY -> OUTSIDE",
            "meaning":
                "The input combination does not satisfy the boundary."
        }

    # ---------------------------------------------------------
    # TRUTH TABLE
    # ---------------------------------------------------------

    def truth_table(self):

        states = [
            BooleanState(0, 0),
            BooleanState(0, 1),
            BooleanState(1, 0),
            BooleanState(1, 1)
        ]

        table = []

        for state in states:

            result = self.classify(state)

            table.append(result)

        return table


# =============================================================
# LOGIC GATES
# =============================================================

AND_GATE = BoundaryLogicGate(
    "AND",
    lambda A, B: A & B
)


OR_GATE = BoundaryLogicGate(
    "OR",
    lambda A, B: A | B
)


XOR_GATE = BoundaryLogicGate(
    "XOR",
    lambda A, B: A ^ B
)


NAND_GATE = BoundaryLogicGate(
    "NAND",
    lambda A, B: 1 - (A & B)
)


NOR_GATE = BoundaryLogicGate(
    "NOR",
    lambda A, B: 1 - (A | B)
)


# =============================================================
# RELATIONAL BOUNDARY ANALYSIS
# =============================================================

def analyze_gate(gate: BoundaryLogicGate):

    print()
    print("=" * 70)
    print(f"RELATIONAL BOUNDARY: {gate.name} GATE")
    print("=" * 70)

    print()
    print("A B | T(X) | Boundary")
    print("----------------------")

    for row in gate.truth_table():

        A, B = row["input"]

        print(
            f"{A} {B} |"
            f"  {row['output']}   |"
            f" {row['boundary']}"
        )

    print()
    print("Many & Few Interpretation")
    print("-" * 30)

    for row in gate.truth_table():

        state = BooleanState(*row["input"])

        interpretation = gate.many_few(state)

        print(
            f"{row['input']} -> "
            f"{interpretation['many_few']}"
        )


# =============================================================
# BOUNDARY LINE
# =============================================================

def boundary_line(A: int, B: int) -> str:
    """
    The boundary line is represented by the AND relation:

        A AND B

    Only the state (1,1) crosses into INSIDE.

    Every other state remains OUTSIDE.
    """

    output = A & B

    if output == 1:
        return "INSIDE"

    return "OUTSIDE"


# =============================================================
# DEMONSTRATE F(X)
# =============================================================

def F(state: BooleanState, gate: BoundaryLogicGate) -> dict:
    """
    F(X) = classification of X relative to the boundary.

    X      = input state
    T(X)   = gate transformation
    F(X)   = boundary classification
    """

    transformed = gate.transform(state)

    if transformed == 1:

        classification = "INSIDE"

    else:

        classification = "OUTSIDE"

    return {
        "X": (state.A, state.B),
        "T(X)": transformed,
        "F(X)": classification
    }


# =============================================================
# MAIN COMPUTATIONAL EXPERIMENT
# =============================================================

if __name__ == "__main__":

    print()
    print("=" * 70)
    print("RELATIONAL BOUNDARY FRAMEWORK")
    print("ACTUAL BOOLEAN COMPUTATIONAL MODEL")
    print("=" * 70)

    print()
    print("AXIOM:")
    print()
    print("{Many & Few}")
    print("    =")
    print("{Boundary Inside}")
    print("+")
    print("{Outside Boundary}")
    print("+")
    print("{Boundary Line}")

    # ---------------------------------------------------------
    # TEST AND GATE
    # ---------------------------------------------------------

    analyze_gate(AND_GATE)

    # ---------------------------------------------------------
    # TEST OR GATE
    # ---------------------------------------------------------

    analyze_gate(OR_GATE)

    # ---------------------------------------------------------
    # TEST XOR GATE
    # ---------------------------------------------------------

    analyze_gate(XOR_GATE)

    # ---------------------------------------------------------
    # DIRECT F(X) TEST
    # ---------------------------------------------------------

    print()
    print("=" * 70)
    print("F(X) DIRECT CLASSIFICATION")
    print("=" * 70)

    states = [
        BooleanState(0, 0),
        BooleanState(0, 1),
        BooleanState(1, 0),
        BooleanState(1, 1)
    ]

    for state in states:

        result = F(state, AND_GATE)

        print(
            f"\nX     = {result['X']}"
            f"\nT(X)  = {result['T(X)']}"
            f"\nF(X)  = {result['F(X)']}"
        )
```
