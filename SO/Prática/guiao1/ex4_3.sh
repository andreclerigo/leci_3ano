#!/bin/bash

x=0123456789
echo ${x:2:4}       # syntax de "{variavel[:indice_comeco][:numero de caracteres impressos]}"
echo ${x/123/ccc}   # syntax de "{variabel[/retirar][/colorcar]}"
