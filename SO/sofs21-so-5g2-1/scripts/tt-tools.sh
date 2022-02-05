#!/bin/bash
# --------------------------------------------------------------------------

function ttai()
{
    helpmsg="ttai [ OPTIONS ]\n"
        helpmsg+="  Allocate one inode in disk $SOFS21_DISK\n"
        helpmsg+="OPTIONS:\n"
        helpmsg+="  -b           --- use binary version\n"
        helpmsg+="  -g           --- use group version\n"
        helpmsg+="  -p           --- probe this function\n"
        helpmsg+="  -v           --- probe all functions\n"
        helpmsg+="  -h           --- this help"

    local list="" 
    local ttoptions="-g" verbose=0
    local permissions
    while [[ $# -gt 0 ]]
    do
        case $1 in 
            "-b"|"-g") # testtool options are the same
                ttoptions+=" $1"
                shift 1
                ;;
            "-p") # probe only this function
                ttoptions+=" -p 401"
                verbose=1
                shift 1
                ;;
            "-v") # probe all functions
                ttoptions+=" -p 0-999"
                verbose=1
                shift 1
                ;;
            "-h") # help message
                InfoMessage "$helpmsg"
                return
                ;;
            *) # some thing wrong
                ErrorMessage "Wrong arguments: \"$@\""
                InfoMessage "$helpmsg"
                break
                ;;
        esac
    done

    if [ $verbose -eq 1 ]; then
        echo -ne "ai\nq\n" | tt -q 1 $ttoptions
    else
        echo $(echo -ne "ai\nq\n" | tt -q 1 $ttoptions -p 0-0 | head -1 | cut -d\  -f3)
    fi
        
}

# --------------------------------------------------------------------------

function ttfi()
{
    helpmsg="ttfi «num» ... [ OPTIONS ]\n"
        helpmsg+="  Free one or more inodes on disk $SOFS21_DISK\n"
        helpmsg+="PARAMETERS:\n"
        helpmsg+="  «num»        --- inode number\n"
        helpmsg+="OPTIONS:\n"
        helpmsg+="  -b           --- use binary version\n"
        helpmsg+="  -g           --- use group version\n"
        helpmsg+="  -p           --- probe this function\n"
        helpmsg+="  -v           --- probe all functions\n"
        helpmsg+="  -h           --- this help"

        WarnMessage "NOT IMPLEMENTED YET"
        InfoMessage "$helpmsg"
}

# --------------------------------------------------------------------------


