#!/bin/bash

touch zzz                                       # to guarantee file zzz exists
test -f zzz && echo "File zzz exists"           # cond1 && cond2 - executa cond2 se cond1 é verdadeiro ($? igual a 0)
rm -f zzz                                       # to guarantee file zzz does not exist
test -f zzz || echo "File zzz does not exist"   # cond1 || cond2 - executa cond2 se con1 é falso ($? diferente de 0)
