#!/bin/bash

rm -f zzz                           # to guarantee file zzz does not exist
if ! test -f zzz
then
    echo "File zzz does not exist"
fi
