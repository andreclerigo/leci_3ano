#!/bin/bash

v=a*        # a* is not expanded in assignment
echo $v     # devolve o valor de $v
echo "$v"   # devolve o comando que criou a variavel $v
echo ’$v’   # devolve a string
