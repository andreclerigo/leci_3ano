#!/bin/bash

declare -A arr
arr["homem"]=man
arr["papel"]=paper
arr["olá"]=hello
arr["lição"]=lesson
echo ${arr[*]}              # the list of elements in the array
echo ${#arr[*]}             # the number of elements in the array
echo ${!arr[*]}             # the list of indices used in the array

for i in ${!arr[*]}
do
    echo "The translation of \"$i\" is \"${arr[$i]}\""
done
