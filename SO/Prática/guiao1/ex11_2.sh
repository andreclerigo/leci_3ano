#!/bin/bash

bash myscript
bash myscript xpto abc for testing
rm -f abc                           # to guarantee it does not exist
bash myscript abc

# create a file for testing
seq -w 100 -3 2 > xpto
bash myscript xpto
