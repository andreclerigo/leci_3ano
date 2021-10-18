#!/bin/bash

check()
{
    if [ -f $1 ]
    then
        echo -e "\e[33mFile zzz exists\e[0m"
    else
        echo -e "\e[31mFile zzz does not exist\e[0m"
    fi
}

touch zzz               # to guarantee file zzz exists
check zzz
rm -f zzz               # to guarantee file zzz does not exist
check zzz
