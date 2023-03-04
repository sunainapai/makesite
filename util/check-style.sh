#!/bin/bash

PEP8_OPTS="--ignore=E221,E501,E241,E266,E203,E126,E201,E202,E121"

clear
pep8 $PEP8_OPTS *.py

exit $?
