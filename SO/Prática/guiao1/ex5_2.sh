#!/bin/bash

y()
{
    echo $#     # the number of arguments
    echo $1     # the first argument
    echo $2     # the second argument
    echo $*     # the list of all arguments
    echo $@     # idem
    echo "$*"   # idem
    echo "$@"   # idem
}
