#! /bin/bash

source sofs21.sh
m
c > /dev/null 2>&1
f -z > /dev/null

for((i=1; i <= 36; i++)); do
    echo -e "ai\nq" | tt -b -q 1 -p 0-0
done;