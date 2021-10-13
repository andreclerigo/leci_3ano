import functools

def main():
    lst = [-1, -2, -3]
    lst_bools = [x > 0 for x in lst]
    
    res = lambda x, y : x | y
    bool = functools.reduce(res, lst_bools)

    print(f'List -> {lst_bools}')
    print(f'Result -> {bool}')


if __name__ == "__main__":
    main()