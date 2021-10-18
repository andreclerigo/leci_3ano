#!/bin/bash

touch a1 a2 a77 abc b1 c12 ddd      # create some files
ls
prefix="_a_"

for f in a*
do
    echo "changing the name of \"$f\""
    mv $f $prefix$f
done
ls
