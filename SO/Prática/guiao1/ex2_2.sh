rm -f zzz       # to guarantee file "zzz" does not exist
cat zzz         # an error message is sent to the terminal display window
cat zzz 2> z    # the error message is sent to file "z",
                # any previous content of "z" being deleted
cat zzz 2>> z   # the error message is appended to the end of file "z"
cat zzz 2> z    # the error message was redirected. Why?
                # file "z" is created if it does not exist
cat zzz > z     # the error message is sent to the terminal display window. Why?
