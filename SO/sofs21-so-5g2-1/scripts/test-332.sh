#!/bin/bash

RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'


# activate scripts and compile code
source sofs21.sh
m -s

printf "${BLUE}\nCreating disk with size 1000\n"
c > /dev/null 2>&1

# format with bin
f -b > /dev/null 2>&1

# write 5 blocks in inode 1
for ((i = 0; i < 5; i++)); do
    echo -e "wib\n1\n$i\n$i\nq\n" | tt -b -q 1 -p 0-0 > /dev/null 2>&1
done;

# remove 2 blocks in inode 1
echo -e "fib\n1\n3\nq\n" | tt -b -q 1 -p 0-0 > /dev/null 2>&1

echo -e "wib\n2\n1\n1\nq\n" | tt -b -q 1 -p 0-0 > /dev/null 2>&1
echo -e "wib\n1\n5\n1\nq\n" | tt -b -q 1 -p 0-0 > /dev/null 2>&1
echo -e "wib\n2\n2\n1\nq\n" | tt -b -q 1 -p 0-0 > /dev/null 2>&1

s -i 1 > ./bin-inodes


# format with grp
f -b -r 332-332 > /dev/null 2>&1

# write 5 blocks in inode 1
for ((i = 0; i < 5; i++)); do
    echo -e "wib\n1\n$i\n$i\nq\n" | tt -b -r 332-332 -q 1 -p 0-0 > /dev/null 2>&1
done;

# remove 2 blocks in inode 1
echo -e "fib\n1\n3\nq\n" | tt -b -r 332-332 -q 1 -p 0-0 > /dev/null 2>&1

echo -e "wib\n2\n1\n1\nq\n" | tt -b -r 332-332 -q 1 -p 0-0 > /dev/null 2>&1
echo -e "wib\n1\n5\n1\nq\n" | tt -b -r 332-332 -q 1 -p 0-0 > /dev/null 2>&1
echo -e "wib\n2\n2\n1\nq\n" | tt -b -r 332-332 -q 1 -p 0-0 > /dev/null 2>&1

s -i 1 > ./grp-inodes


# check if the outputs match for the inodes
out=$(diff ./grp-inodes ./bin-inodes)
if [[ $out -eq 0 ]]; then
    printf "${GREEN}Passed for a disk with 1000 blocks (same inodes)\n";
    rm grp-inodes bin-inodes
else
    printf "${RED}Error different inodes: function failed for a disk with 1000 blocks (output files saved)\n";
    exit 1;
fi
