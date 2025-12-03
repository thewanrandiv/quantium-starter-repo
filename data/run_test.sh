#!/bin/bash

# Bash script to run Dash app test suite
# Exit codes: 0 = success, 1 = failure

set -e  # Exit on any error

echo "=========================================="
echo "Starting Soul Foods Test Suite"
echo "=========================================="

# Step 1: Activate virtual environment
echo "Activating virtual environment..."

# Check for common virtual environment names
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "✓ Activated venv"
elif [ -d ".venv" ]; then
    source .venv/bin/activate
    echo "✓ Activated .venv"
elif [ -d "env" ]; then
    source env/bin/activate
    echo "✓ Activated env"
else
    echo "✗ Error: No virtual environment found (venv, .venv, or env)"
    echo "Please create a virtual environment first:"
    echo "  python -m venv venv"
    exit 1
fi

# Verify activation
if [ -z "$VIRTUAL_ENV" ]; then
    echo "✗ Error: Virtual environment activation failed"
    exit 1
fi

echo "Virtual environment: $VIRTUAL_ENV"
echo ""

# Step 2: Execute test suite
echo "Running test suite..."
echo "------------------------------------------"

# Run pytest and capture exit code
pytest test_app.py -v --tb=short

# Step 3: Check exit code and return appropriate value
TEST_EXIT_CODE=$?

echo ""
echo "=========================================="

if [ $TEST_EXIT_CODE -eq 0 ]; then
    echo "✓ All tests passed successfully!"
    echo "=========================================="
    exit 0
else
    echo "✗ Tests failed with exit code: $TEST_EXIT_CODE"
    echo "=========================================="
    exit 1
fi