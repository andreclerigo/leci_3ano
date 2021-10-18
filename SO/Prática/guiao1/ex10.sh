#!/bin/bash


f2()
{
    while [ $# -gt 0 ]
    do
        echo "==== $1 ====" > $1
        shift
    done
}

f3()
{
    until [ $# -eq 0 ]
    do
        echo "==== $1 ====" > $1
        shift
    done
}

rm -f abc xpto zzz      # to guarantee they do not exist
f2 abc xpto zzz
cat xpto
cat abc
cat zzz
f3 abc xpto zzz
cat xpto
cat abc
cat zzz
