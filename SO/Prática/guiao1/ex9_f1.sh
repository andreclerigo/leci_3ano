#!/bin/bash

f1()
{
    for file in $*
    do
        echo "=== $file ===" > $file
    done
}

f1 abc xpto zzz
cat xpto
cat abc
cat zzz
