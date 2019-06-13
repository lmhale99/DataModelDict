#!/bin/bash

# Build README.rst
sphinx-build -b rst .sphinx_source .

# Correct README.rst
python readme_fix.py