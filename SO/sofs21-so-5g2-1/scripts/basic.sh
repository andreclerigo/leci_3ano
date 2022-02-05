#!/bin/bash
# --------------------------------------------------------------------------

# Create the $SOFS21_DISK disk with the given number of blocks (default 1000)
function c() 
{ 
    local sz;
    if [ $# -eq 0 ]; then
        sz=1000
    else
        sz=$1
    fi;
    local cwd="$(pwd)"
    cd "$SOFS21_ROOT/bin"
    ./createDisk "$SOFS21_DISK" $sz
    local ret=$?
    cd $cwd
    return $ret
}

# --------------------------------------------------------------------------

# Call mksofs on $SOFS21_DISK disk
# By default it uses group version and maximum probing
# format
function f()
{
    local cwd="$(pwd)"
    cd "$SOFS21_ROOT/bin"
    ./mksofs -g -p 0-999 "$SOFS21_DISK" $@
    local ret=$?
    cd $cwd
    return $ret
}

# --------------------------------------------------------------------------

# Call showblock on $SOFS21_DISK disk
function s()
{
    local cwd="$(pwd)"
    cd "$SOFS21_ROOT/bin"
    ./showblock "$SOFS21_DISK" $@
    local ret=$?
    cd $cwd
    return $ret
}

# --------------------------------------------------------------------------

# Call testtool on $SOFS21_DISK disk
# By default it uses group version and maximum probing
function tt()
{
    local cwd="$(pwd)"
    cd "$SOFS21_ROOT/bin"
    ./testtool -g  -p 0-999 "$SOFS21_DISK" $@
    local ret=$?
    cd $cwd
    return $ret
}

# --------------------------------------------------------------------------

# Call make/ninja on build folder
function m()
{
    # check if build directory exists 
    if ! [ -d "$SOFS21_ROOT/build" ]; then
        ErrorMessage "Directory $SOFS21_ROOT/build doe not exist. Aborting."
        return 1
    fi
    # call make/ninja
    local cwd=$(pwd)
    cd "$SOFS21_ROOT/build"
    if [ -f Makefile ]; then
        make $@
    elif [ -f rules.ninja ]; then
        ninja $@
    else
        WarnMessage "cmake needs to be configured first"
    fi
    cd "$cwd"
}

# --------------------------------------------------------------------------

