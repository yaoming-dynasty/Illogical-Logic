#!/usr/bin/env bash

# ============================================================
# certify.sh
# RELATIONAL PROOF OF AUTHORSHIP / CONTENT COMMITMENT
#
# Author:
#     Christopher Thomas Ronio
#
# Framework:
#     Relational Boundary Framework
#
# Pipeline:
#
#     X
#      |
#      v
#     T(X)
#      |
#      v
#     F(X)
#      |
#      v
#     Canonical Certificate
#      |
#      v
#     SHA-256
#      |
#      v
#     Commitment
#
# IMPORTANT:
#     The commitment is calculated over the canonical
#     certificate with the "commitment" field set to null.
#
#     This prevents a circular hash dependency.
#
#     SHA-256 proves content integrity/commitment.
#     It does not independently establish legal authorship.
# ============================================================

set -euo pipefail

AUTHOR="Christopher Thomas Ronio"
FRAMEWORK="Relational Boundary Framework"

INPUT_FILE="${1:-Algebraic.md}"
OUTPUT_FILE="${2:-rpa_certificate.json}"

echo "========================================================"
echo " RELATIONAL PROOF OF AUTHORSHIP / CONTENT COMMITMENT"
echo "========================================================"
echo " Author:    ${AUTHOR}"
echo " Framework: ${FRAMEWORK}"
echo " File:      ${INPUT_FILE}"
echo "========================================================"


# ============================================================
# VALIDATE PYTHON
# ============================================================

if ! command -v python3 >/dev/null 2>&1; then
    echo "[!] Error: python3 could not be found."
    exit 1
fi


# ============================================================
# VALIDATE INPUT
# ============================================================

if [[ ! -f "${INPUT_FILE}" ]]; then
    echo "[!] Error: File not found: ${INPUT_FILE}"
    exit 1
fi

echo "[+] Input file verified."


# ============================================================
# EXECUTE RELATIONAL FRAMEWORK
# ============================================================

RPA_RESULT_FILE="$(mktemp)"

cleanup() {
    rm -f "${RPA_RESULT_FILE}"
}

trap cleanup EXIT


if [[ -f "Examples/rpa_framework.py" ]]; then

    echo "[*] Executing relational boundary framework..."

    python3 Examples/rpa_framework.py \
        --file "${INPUT_FILE}" \
        --json > "${RPA_RESULT_FILE}"

else

    echo "[!] Examples/rpa_framework.py was not found."

    echo "{" > "${RPA_RESULT_FILE}"
    echo '  "classification": "UNAVAILABLE",' >> "${RPA_RESULT_FILE}"
    echo '  "error": "Framework execution file not found."' >> "${RPA_RESULT_FILE}"
    echo "}" >> "${RPA_RESULT_FILE}"

fi


# ============================================================
# GENERATE CANONICAL CERTIFICATE
# ============================================================

python3 - \
    "${AUTHOR}" \
    "${FRAMEWORK}" \
    "${INPUT_FILE}" \
    "${RPA_RESULT_FILE}" \
    "${OUTPUT_FILE}" <<'PY'

import hashlib
import json
import pathlib
import sys
from datetime import datetime, timezone


# ------------------------------------------------------------
# Arguments
# ------------------------------------------------------------

author = sys.argv[1]
framework = sys.argv[2]
input_file = pathlib.Path(sys.argv[3])
result_file = pathlib.Path(sys.argv[4])
output_file = pathlib.Path(sys.argv[5])


# ------------------------------------------------------------
# Hash source document
# ------------------------------------------------------------

file_hash = hashlib.sha256(
    input_file.read_bytes()
).hexdigest()


# ------------------------------------------------------------
# Read F(X) result
# ------------------------------------------------------------

try:

    framework_result = json.loads(
        result_file.read_text(encoding="utf-8")
    )

except json.JSONDecodeError:

    framework_result = {
        "classification": "INVALID_FRAMEWORK_RESULT"
    }


# ------------------------------------------------------------
# Canonical timestamp
# ------------------------------------------------------------

timestamp = datetime.now(
    timezone.utc
).strftime("%Y-%m-%dT%H:%M:%SZ")


# ------------------------------------------------------------
# Extract F(X)
#
# The framework should ideally return:
#
# {
#     "classification": "...",
#     "state": "...",
#     "behavior_history": [...],
#     "iterations": ...
# }
# ------------------------------------------------------------

f_x = {
    "classification":
        framework_result.get(
            "classification",
            "UNAVAILABLE"
        ),

    "state":
        framework_result.get(
            "state"
        ),

    "iterations":
        framework_result.get(
            "iterations"
        ),

    "cycle_length":
        framework_result.get(
            "cycle_length"
        ),

    "behavior_history":
        framework_result.get(
            "behavior_history",
            []
        )
}


# ------------------------------------------------------------
# RELATIONAL BOUNDARY
#
# This records the computational interpretation of F(X).
# ------------------------------------------------------------

boundary = {

    "inside":
        "F(X) = INSIDE",

    "outside":
        "F(X) = OUTSIDE",

    "line":
        "T(X) -> F(X)",

    "classification":
        f_x["classification"]

}


# ------------------------------------------------------------
# CANONICAL CERTIFICATE
#
# IMPORTANT:
#
# "commitment": None is intentional.
#
# This exact structure is what gets hashed.
# The resulting SHA-256 digest is then inserted into
# the final certificate.
# ------------------------------------------------------------

certificate = {

    "certificate_type":
        "RELATIONAL_PROOF_OF_AUTHORSHIP",

    "certificate_version":
        "1.0",

    "author_claim":
        author,

    "framework":
        framework,

    "source": {

        "file":
            input_file.name,

        "sha256":
            file_hash

    },

    "relational_model": {

        "X":
            input_file.name,

        "T(X)":
            "Relational Boundary Transformation",

        "F(X)":
            f_x,

        "boundary":
            boundary

    },

    "timestamp_utc":
        timestamp,

    "verification": {

        "hash_algorithm":
            "SHA-256",

        "canonicalization":
            "JSON sorted keys, UTF-8, compact separators",

        "commitment_scope":
            "Complete certificate payload with commitment=null"

    },

    # Reserved during hashing.
    "commitment":
        None

}


# ------------------------------------------------------------
# CANONICAL SERIALIZATION
# ------------------------------------------------------------

canonical_bytes = json.dumps(
    certificate,
    sort_keys=True,
    separators=(",", ":"),
    ensure_ascii=False
).encode("utf-8")


# ------------------------------------------------------------
# CALCULATE CERTIFICATE COMMITMENT
# ------------------------------------------------------------

certificate_hash = hashlib.sha256(
    canonical_bytes
).hexdigest()


# ------------------------------------------------------------
# INSERT COMMITMENT
# ------------------------------------------------------------

certificate["commitment"] = {

    "algorithm":
        "SHA-256",

    "digest":
        certificate_hash

}


# ------------------------------------------------------------
# WRITE FINAL CERTIFICATE
# ------------------------------------------------------------

output_file.write_text(
    json.dumps(
        certificate,
        indent=4,
        sort_keys=True,
        ensure_ascii=False
    ) + "\n",
    encoding="utf-8"
)


# ------------------------------------------------------------
# OUTPUT
# ------------------------------------------------------------

print()
print("[+] RELATIONAL CERTIFICATE GENERATED")
print()
print(f"    Author:       {author}")
print(f"    Source:       {input_file.name}")
print(f"    File SHA-256: {file_hash}")
print(f"    F(X):         {f_x['classification']}")
print(f"    Certificate:  {certificate_hash}")
print(f"    Output:       {output_file}")
print()

PY


# ============================================================
# FINAL REPORT
# ============================================================

echo "========================================================"
echo " RELATIONAL CERTIFICATION COMPLETE"
echo "========================================================"
echo " Author:      ${AUTHOR}"
echo " Framework:   ${FRAMEWORK}"
echo " Source:      ${INPUT_FILE}"
echo " Certificate: ${OUTPUT_FILE}"
echo "========================================================"
echo ""
echo "F(X) is included in the canonical certificate payload."
echo "The certificate commitment is the SHA-256 digest of"
echo "that canonical payload with commitment=null."
echo ""
echo "This provides deterministic content verification."
echo "It does not independently establish legal authorship."
echo "========================================================"
