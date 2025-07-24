#!/bin/bash

# Quick Fix Script for T-Developer v1.1

echo "Running quick fixes..."

# The registry methods were already added in previous commits
# Let's verify they exist
echo "Checking registry methods..."
grep -n "def get(" tdev/core/registry.py
grep -n "def get_by_type(" tdev/core/registry.py

# Run tests with coverage
echo "Running tests with coverage..."
pytest --cov=tdev tests/ -v

# Generate coverage report
echo "Generating coverage report..."
coverage html

echo "Quick fixes completed!"