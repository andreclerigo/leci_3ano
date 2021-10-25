#!/bin/bash
# -----------------------------------------------------------------------------------

sofs21_setup()
{
    # create some useful env variables
    cd "$(dirname ${BASH_SOURCE[0]})"
    export SOFS21_SCRIPTS="$(pwd)"
    cd ..
    export SOFS21_ROOT="$(pwd)"
    export SOFS21_BIN="$(pwd)/bin"
    
    export SOFS21_DISK="/tmp/dsk"

    # source bash tools
    source "$SOFS21_SCRIPTS/msg.sh"
    source "$SOFS21_SCRIPTS/basic.sh"
}

# -----------------------------------------------------------------------------------

# bash command to resource bash tools in case they were edited
rs()
{
    source $SOFS21_SCRIPTS/sofs21.sh
}

sofs21_setup

# -----------------------------------------------------------------------------------

