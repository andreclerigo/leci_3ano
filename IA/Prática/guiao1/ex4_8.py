import functools

def main():
    lst1 = [1, 2, 3, 4]
    lst2 = [1, 2, 3]

    lst_bools = [x in lst2 for x in lst1]
    
    res = lambda x, y : x & y
    bool = functools.reduce(res, lst_bools)

    print(f'List -> {lst_bools}')
    print(f'Result -> {bool}')

if __name__ == '__main__':
    main()