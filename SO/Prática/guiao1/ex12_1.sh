#|/bin/bash

a[1]=aaa
echo ${a[1]}
declare -a a[2]=bbb         # can also be used
a[4]=ddd
a[2+3]=eee                  # integer arithmetic expression are allowed
echo ${a[*]}                # the list of elements in the array
echo ${#a[*]}               # the number of elements in the array
echo ${!a[*]}               # the list of indices used in the array

# iterate through the list of elements
for v in ${a[*]}
do
    echo $v
done

# iterate through the list of indices
for i in ${!a[*]}
do
    echo "a[$i] = ${a[$i]}"
done
