#!/bin/bash

RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'

block_sizes=(5 10 30 1000 998 8992 10000 20000 20003)

# activate scripts and compile code
source sofs21.sh
m -s

function test_445_without_fdb_adb() {
    # set the argument
    size=$1

    printf "${BLUE}\nCreating disk with size ${size}\n"
    c $1 > /dev/null 2>&1
    
    # format with bin
    f -b > /dev/null 2>&1
    index_bitmap=$(s | grep "First block of the bitmap table: " | cut -d: -f2 | xargs)
    bitmap_blocks=$(s | grep "Number of blocks of the bitmap table: " | cut -d: -f2 | xargs)

    # RFB with bin
    echo -e "rfb\nq\n" | tt -b -q 1 -p 0-0 > /dev/null 2>&1
    for ((i = $index_bitmap; i < $index_bitmap + $bitmap_blocks; i++)); do
        echo "bitmap block $i for size $1" >> ./bin-format-bitmap
        s -b $i >> ./bin-format-bitmap
    done
    
    # check cache content
    cache_content=$(s | sed -n -e "/Retrieval cache:/,/Insertion cache:/ p")
    echo "cache for size $1\n" >> ./bin-format-cache
    echo "$cache_content" >> ./bin-format-cache


    # format with grp
    f -b -r 445-445 > /dev/null 2>&1
    index_bitmap=$(s | grep "First block of the bitmap table: " | cut -d: -f2 | xargs)
    bitmap_blocks=$(s | grep "Number of blocks of the bitmap table: " | cut -d: -f2 | xargs)

    # RFB with grp
    echo -e "rfb\nq\n" | tt -b -r 445-445 -q 1 -p 0-0 > /dev/null 2>&1
    for ((i = $index_bitmap; i < $index_bitmap + $bitmap_blocks; i++)); do
        echo "bitmap block $i for size $1" >> ./grp-format-bitmap
        s -b $i >> ./grp-format-bitmap
    done
    cache_content=$(s | sed -n -e "/Retrieval cache:/,/Insertion cache:/ p")
    echo "cache for size $1\n" >> ./grp-format-cache
    echo "$cache_content" >> ./grp-format-cache

    
    # check if the outputs match for the bitmap
    out=$(diff ./grp-format-bitmap ./bin-format-bitmap)
    if [[ $out -eq 0 ]]; then
        printf "${GREEN}Passed for a disk with ${size} blocks (same bitmap)\n";
        rm grp-format-bitmap bin-format-bitmap
    else
        printf "${RED}Error different bitmap: function failed for a disk with ${size} blocks (output files saved)\n";
        exit 1;
    fi

    # check if the outputs match for the cache
    out=$(diff ./grp-format-cache ./bin-format-cache)
    if [[ $out -eq 0 ]]; then
        printf "${GREEN}Passed for a disk with ${size} blocks (same cache)\n";
        rm grp-format-cache bin-format-cache
    else
        printf "${RED}Error different cache: function failed for a disk with ${size} blocks (output files saved)\n";
        exit 1;
    fi
}

function test_445_with_fdb_adb() {
    # set the argument
    size=$1

    printf "${BLUE}\nCreating disk with size ${size}\n"
    c $1 > /dev/null 2>&1
    
    # bin
    f -b > /dev/null 2>&1
    echo -e "rfb\nq\n" | tt -b -q 1 -p 0-0 > /dev/null 2>&1

    for ((i = 0; i < 180; i++)); do
        echo -e "adb\nq\n" | tt -b -q 1 -p 0-0 > /dev/null 2>&1
    done

    for i in {1..130..2}
      do
        echo -e "fdb\n$i\nq\n" | tt -b -q 1 -p 0-0 > /dev/null 2>&1
    done

    s -b 5 > ./bin-format-bitmap


    # grp
    f -b -r 445-445 > /dev/null 2>&1
    echo -e "rfb\nq\n" | tt -b -r 445-445 -q 1 -p 0-0 > /dev/null 2>&1

    for ((i = 0; i < 180; i++)); do
        echo -e "adb\nq\n" | tt -b -r 445-445 -q 1 -p 0-0 > /dev/null 2>&1
    done

    for i in {1..130..2}
      do
        echo -e "fdb\n$i\nq\n" | tt -b -r 445-445 -q 1 -p 0-0 > /dev/null 2>&1
    done

    s -b 5 > ./grp-format-bitmap


    # check if the outputs match for the bitmap
    out=$(diff ./grp-format-bitmap ./bin-format-bitmap)
    if [[ $out -eq 0 ]]; then
        printf "${GREEN}Passed for a disk with ${size} blocks (same bitmap)\n";
        rm grp-format-bitmap bin-format-bitmap
    else
        printf "${RED}Error different bitmap: function failed for a disk with ${size} blocks (output files saved)\n";
        exit 1;
    fi
}

# test for each block size with no allocs and frees
printf "${YELLOW}\nTesting RFB";
for size in ${block_sizes[@]}; do
    test_445_without_fdb_adb $size
done

printf "${YELLOW}\nTesting RFB with 180 Allocs and 65 Frees";
test_445_with_fdb_adb 1000