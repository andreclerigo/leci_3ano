rm -f zzz                   # to guarantee zzz does not exist
cat zzz > err               # nao acontece nada porque cat zzz é erro e vai para o stderr
cat zzz > err 2>&1          # funciona porque mudamos o err (2>) pata o out (&1)
cat err
cat /etc/passwd 2> z        # como o comando nao da err vai para o stdout estamos a dar o input do stderr nao acontece nada
cat /etc/passwd 2> z >&2    # trocamos o stdout pelo stderr
