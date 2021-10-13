def remove(lst, n):
    if lst == []:
        return []

    if lst[0] != n:
        return [lst[0]] + remove(lst[1:], n)
    return remove(lst[1:], n)   

def main():
    lst = [-20, 5, -2, 5, 2, 1, 19, 14, 2, 5]
    n = int(input("Remove: "))
    filtered_lst = remove(lst, n)
    tup = (filtered_lst, n)
    print(tup)

if __name__ == '__main__':
    main()