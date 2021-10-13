def concat(lst):
    if lst == []:
        return []

    concat_lst = lst[0] + concat(lst[1:])    

    return concat_lst

def main():
    lst = [[1, 2, 3],[4], [],[3, 2], [1, 20, 100], []]
    print(concat(lst))

if __name__ == '__main__':
    main()
