import functools

def main():
    lst = [1, 2, 3]
    
    bool_func = lambda x : x > 0
    lst_bools = list(map(bool_func, lst))
    
    res = lambda x, y : x & y
    bool = functools.reduce(res, lst_bools)

    print(f'List -> {lst_bools}')
    print(f'Result -> {bool}')


if __name__ == "__main__":
    main()