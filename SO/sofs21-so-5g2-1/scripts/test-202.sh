#!/bin/bash

RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'


# activate scripts and compile code
source sofs21.sh
m -s

function test_202_oneslot() {
    c > /dev/null 2>&1
    
    # format with bin
    f -b > /dev/null 2>&1
    
    # testing directory that occupies one DIRECTORY_SLOT
    echo -e "ai\nq\n" | tt -b -q 1 -p 0-0 > /dev/null 2>&1
    echo -e "ai\nq\n" | tt -b -q 1 -p 0-0 > /dev/null 2>&1
    echo -e "ade\n0\nabc\n1\nq\n" | tt -b -q 1 -p 0-0 > /dev/null 2>&1
    echo -e "ade\n0\nabcd\n1\nq\n" | tt -b -q 1 -p 0-0 > /dev/null 2>&1
    echo -e "ade\n0\nabcde\n1\nq\n" | tt -b -q 1 -p 0-0 > /dev/null 2>&1
    echo -e "ade\n0\nabcdef\n1\nq\n" | tt -b -q 1 -p 0-0 > /dev/null 2>&1
    echo -e "dde\n0\nabcd\nq\n" | tt -b -q 1 -p 0-0 > /dev/null 2>&1
    echo -e "dde\n0\nabcde\nq\n" | tt -b -q 1 -p 0-0 > /dev/null 2>&1
    echo -e "ade\n0\nteste\n2\nq\n" | tt -b -q 1 -p 0-0 > /dev/null 2>&1

    # get the directory content
    s -d 6 > ./bin-dirs
    s -i 1 >> ./bin-dirs

    # format with bin
    f -b -r 202-202 > /dev/null 2>&1
    
    # testing directory that occupies one DIRECTORY_SLOT
    echo -e "ai\nq\n" | tt -b -r 202-202 -q 1 -p 0-0 > /dev/null 2>&1
    echo -e "ai\nq\n" | tt -b -r 202-202 -q 1 -p 0-0 > /dev/null 2>&1
    echo -e "ade\n0\nabc\n1\nq\n" | tt -b -r 202-202 -q 1 -p 0-0 > /dev/null 2>&1
    echo -e "ade\n0\nabcd\n1\nq\n" | tt -b -r 202-202 -q 1 -p 0-0 > /dev/null 2>&1
    echo -e "ade\n0\nabcde\n1\nq\n" | tt -b -r 202-202 -q 1 -p 0-0 > /dev/null 2>&1
    echo -e "ade\n0\nabcdef\n1\nq\n" | tt -b -r 202-202 -q 1 -p 0-0 > /dev/null 2>&1
    echo -e "dde\n0\nabcd\nq\n" | tt -b -r 202-202 -q 1 -p 0-0 > /dev/null 2>&1
    echo -e "dde\n0\nabcde\nq\n" | tt -b -r 202-202 -q 1 -p 0-0 > /dev/null 2>&1
    echo -e "ade\n0\nteste\n2\nq\n" | tt -b -r 202-202 -q 1 -p 0-0 > /dev/null 2>&1

    # get the directory content
    s -d 6 > ./grp-dirs
    s -i 1 >> ./grp-dirs

    # check if the outputs match
    out=$(diff ./grp-dirs ./bin-dirs)
    if [[ $out -eq 0 ]]; then
        printf "\n${GREEN}Passed for dirs that occupy one DIRECTORY_SLOT\n";
        rm grp-dirs bin-dirs
    else
        printf "\n${RED}Error: function failed for dirs that occupy one DIRECTORY_SLOT (output files saved)\n";
        exit 1;
    fi
}

function test_202_twoslots() {
    c > /dev/null 2>&1
    
    # format with bin
    f -b > /dev/null 2>&1
    
    # testing directory that occupies one DIRECTORY_SLOT
    echo -e "ai\nq\n" | tt -b -q 1 -p 0-0 > /dev/null 2>&1
    echo -e "ai\nq\n" | tt -b -q 1 -p 0-0 > /dev/null 2>&1
    echo -e "ade\n0\nabc\n1\nq\n" | tt -b -q 1 -p 0-0 > /dev/null 2>&1
    echo -e "ade\n0\naaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\n1\nq\n" | tt -b -q 1 -p 0-0 > /dev/null 2>&1
    echo -e "ade\n0\nbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb\n1\nq\n" | tt -b -q 1 -p 0-0 > /dev/null 2>&1
    echo -e "ade\n0\nccccccccccccccccccccccccccccccc\n1\nq\n" | tt -b -q 1 -p 0-0 > /dev/null 2>&1
    echo -e "dde\n0\nabc\nq\n" | tt -b -q 1 -p 0-0 > /dev/null 2>&1
    echo -e "ade\n0\nddddddddddddddddddddddddddddddd\n2\nq\n" | tt -b -q 1 -p 0-0 > /dev/null 2>&1
    echo -e "dde\n0\nbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb\nq\n" | tt -b -q 1 -p 0-0 > /dev/null 2>&1
    echo -e "ade\n0\neeeeeeeeeeeeeeeeeeeeeeeeeeeeeee\n2\nq\n" | tt -b -q 1 -p 0-0 > /dev/null 2>&1

    # get the directory content
    s -d 6 > ./bin-dirs
    s -i 1 >> ./bin-dirs

    # format with bin
    f -b -r 202-202 > /dev/null 2>&1
    
    # testing directory that occupies one DIRECTORY_SLOT
    echo -e "ai\nq\n" | tt -b -r 202-202 -q 1 -p 0-0 > /dev/null 2>&1
    echo -e "ai\nq\n" | tt -b -r 202-202 -q 1 -p 0-0 > /dev/null 2>&1
    echo -e "ade\n0\nabc\n1\nq\n" | tt -b -r 202-202 -q 1 -p 0-0 > /dev/null 2>&1
    echo -e "ade\n0\naaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\n1\nq\n" | tt -b -r 202-202 -q 1 -p 0-0 > /dev/null 2>&1
    echo -e "ade\n0\nbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb\n1\nq\n" | tt -b -r 202-202 -q 1 -p 0-0 > /dev/null 2>&1
    echo -e "ade\n0\nccccccccccccccccccccccccccccccc\n1\nq\n" | tt -b -r 202-202 -q 1 -p 0-0 > /dev/null 2>&1
    echo -e "dde\n0\nabc\nq\n" | tt -b -r 202-202 -q 1 -p 0-0 > /dev/null 2>&1
    echo -e "ade\n0\nddddddddddddddddddddddddddddddd\n2\nq\n" | tt -b -r 202-202 -q 1 -p 0-0 > /dev/null 2>&1
    echo -e "dde\n0\nbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb\nq\n" | tt -b -r 202-202 -q 1 -p 0-0 > /dev/null 2>&1
    echo -e "ade\n0\neeeeeeeeeeeeeeeeeeeeeeeeeeeeeee\n2\nq\n" | tt -b -r 202-202 -q 1 -p 0-0 > /dev/null 2>&1

    # get the directory content
    s -d 6 > ./grp-dirs
    s -i 1 >> ./grp-dirs

    # check if the outputs match
    out=$(diff ./grp-dirs ./bin-dirs)
    if [[ $out -eq 0 ]]; then
        printf "\n${GREEN}Passed for dirs that occupy two DIRECTORY_SLOTs\n";
        rm grp-dirs bin-dirs
    else
        printf "\n${RED}Error: function failed for dirs that occupy two DIRECTORY_SLOTs (output files saved)\n";
        exit 1;
    fi
}

function test_202_40oneslot() {
    c > /dev/null 2>&1
    
    # format with bin
    f -b > /dev/null 2>&1
    
    # testing directory that occupies one DIRECTORY_SLOT
    echo -e "ai\nq\n" | tt -b -q 1 -p 0-0 > /dev/null 2>&1
    for ((i = 0; i < 40; i++)); do
        echo -e "ade\n0\n$i\n1\nq\n" | tt -b -q 1 -p 0-0 > /dev/null 2>&1
    done

    # get the directory content
    s -d 6 > ./bin-dirs
    s -d 7 >> ./bin-dirs
    s -i 1 >> ./bin-dirs

    #format with bin
    f -b -r 202-202 > /dev/null 2>&1
    
    # testing directory that occupies one DIRECTORY_SLOT
    echo -e "ai\nq\n" | tt -b -r 202-202 -q 1 -p 0-0 > /dev/null 2>&1
    for ((i = 0; i < 40; i++)); do
        echo -e "ade\n0\n$i\n1\nq\n" | tt -b -r 202-202 -q 1 -p 0-0 > /dev/null 2>&1
    done

    # get the directory content
    s -d 6 > ./grp-dirs
    s -d 7 >> ./grp-dirs
    s -i 1 >> ./grp-dirs

    # check if the outputs match
    out=$(diff ./grp-dirs ./bin-dirs)
    if [[ $out -eq 0 ]]; then
        printf "\n${GREEN}Passed for 30+ dirs that occupy one DIRECTORY_SLOT\n";
        rm grp-dirs bin-dirs
    else
        printf "\n${RED}Error: function failed for 30+ dirs that occupy one DIRECTORY_SLOT (output files saved)\n";
        exit 1;
    fi
}

function test_202_40twoslot() {
    c > /dev/null 2>&1
    
    # format with bin
    f -b > /dev/null 2>&1
    
    # testing directory that occupies two DIRECTORY_SLOTs
    echo -e "ai\nq\n" | tt -b -q 1 -p 0-0 > /dev/null 2>&1
    for ((i = 0; i < 20; i++)); do
        echo -e "ade\n0\naaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa$i\n1\nq\n" | tt -b -q 1 -p 0-0 > /dev/null 2>&1
    done

    # get the directory content
    s -d 6 > ./bin-dirs
    s -d 7 >> ./bin-dirs
    s -i 1 >> ./bin-dirs

    # format with bin
    f -b -r 202-202 > /dev/null 2>&1
    
    # testing directory that occupies two DIRECTORY_SLOTs
    echo -e "ai\nq\n" | tt -b -r 202-202 -q 1 -p 0-0 > /dev/null 2>&1
    for ((i = 0; i < 20; i++)); do
        echo -e "ade\n0\naaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa$i\n1\nq\n" | tt -b -r 202-202 -q 1 -p 0-0 > /dev/null 2>&1
    done

    # get the directory content
    s -d 6 > ./grp-dirs
    s -d 7 >> ./grp-dirs
    s -i 1 >> ./grp-dirs

    # check if the outputs match
    out=$(diff ./grp-dirs ./bin-dirs)
    if [[ $out -eq 0 ]]; then
        printf "\n${GREEN}Passed for 30+ dirs that occupy two DIRECTORY_SLOTs\n";
        rm grp-dirs bin-dirs
    else
        printf "\n${RED}Error: function failed for 30+ dirs that occupy two DIRECTORY_SLOTs (output files saved)\n";
        exit 1;
    fi
}

# test direntries
test_202_oneslot
test_202_twoslots
test_202_40oneslot
test_202_40twoslot
