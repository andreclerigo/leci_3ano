#! /bin/bash

source sofs21.sh
m
c > /dev/null 2>&1
f -z > /dev/null

for((i=1; i < 61; i++)); do
    echo -e "adb\nq" | tt -b -q 1 -p 0-0
    echo -e "fdb\n$i\nq" | tt -b -q 1 -p 0-0
done;