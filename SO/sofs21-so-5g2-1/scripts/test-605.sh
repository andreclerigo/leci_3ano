#!/bin/bash

RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'

block_sizes=(1000 998 8992 10000 20000 20003)

# activate scripts and compile code
source sofs21.sh
m -s

function test_605() {
    # set the argument
    size=$1

    printf "${BLUE}\nCreating disk with size ${size}\n"
    c $1 > /dev/null 2>&1
    
    # format with bin
    f -b > /dev/null 2>&1
    index_bitmap=$(s | grep "First block of the bitmap table: " | cut -d: -f2 | xargs)
    bitmap_blocks=$(s | grep "Number of blocks of the bitmap table: " | cut -d: -f2 | xargs)
    printf "${YELLOW}Index of bitmap: $index_bitmap\n"
    printf "${YELLOW}Bitmap blocks: $bitmap_blocks\n"

    for ((i = $index_bitmap; i < $index_bitmap + $bitmap_blocks; i++)); do
        s -b $i >> ./bin-format
    done

    # format with grp
    f -b -r 605-605 > /dev/null 2>&1
    index_bitmap=$(s | grep "First block of the bitmap table: " | cut -d: -f2 | xargs)
    bitmap_blocks=$(s | grep "Number of blocks of the bitmap table: " | cut -d: -f2 | xargs)
    for ((i = $index_bitmap; i < $index_bitmap + $bitmap_blocks; i++)); do
        s -b $i >> ./grp-format
    done
    
    # check if the outputs match
    out=$(diff ./grp-format ./bin-format)
    if [[ $out -eq 0 ]]; then
        printf "${GREEN}Passed for a disk with ${size} blocks\n";
        rm grp-format bin-format
    else
        printf "${RED}Error: function failed for a disk with ${size} blocks (output files saved)\n";
        exit 1;
    fi
}

# test for each block size
for size in ${block_sizes[@]}; do
    test_605 $size
done
