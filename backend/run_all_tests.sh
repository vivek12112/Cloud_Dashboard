#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"
source venv/bin/activate
echo "Running automated tests with pytest..."
python run_tests_and_report.py
