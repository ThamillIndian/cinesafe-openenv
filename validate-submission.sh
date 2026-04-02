#!/bin/bash
# validate-submission.sh – OpenEnv Submission Verifier

set -uo pipefail

# Mandatory checks for the submission
echo "Starting Submission Validation..."

# 1. Spec compliance
if [ ! -f "openenv.yaml" ]; then echo "Missing openenv.yaml"; exit 1; fi
if [ ! -f "Dockerfile" ]; then echo "Missing Dockerfile"; exit 1; fi
if [ ! -f "inference.py" ]; then echo "Missing inference.py"; exit 1; fi
if [ ! -f "uv.lock" ]; then echo "Missing uv.lock - run 'uv lock' to generate it"; exit 1; fi
if [ ! -f "server/app.py" ]; then echo "Missing server/app.py - required for multi-mode deployment"; exit 1; fi

# 2. Package verification
echo "Running Unit Tests..."
pytest tests/test_env.py --cov=cinesafe_openenv

# 3. Environment variable checks
if [ -z "${HF_TOKEN:-}" ]; then echo "Warning: HF_TOKEN is not set. Inference might fail."; fi

# 4. Dry-run inference
echo "Running dry-run inference..."
PYTHONPATH=. python inference.py

# 5. Result Verification
echo "Success! Submission is ready for packaging."
