#!/bin/sh

set -x
set -e

# pycodestyle --format=pylint --show-pep8 *.py
flake8 --format=pylint --max-line-length=120 --extend-ignore=E111,E114,E231,E203,E741,E731,E251,E252,F821,F722 *.py

# Run some tests.
./edag.py
./edag_components.py
./edag_utils.py
./edag_dcdc.py
./test.py

# Regenerate Sphinx documentation.
cd doc && make html
