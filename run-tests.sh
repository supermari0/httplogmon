#!/bin/bash
python3 -m unittest discover $( dirname "${BASH_SOURCE[0]}") "test_*.py"
