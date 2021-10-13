def head(lst):
    if lst == []:
        return None

    return lst[0]

def main():
    lst = [-20, 5, -2, 5, 2, 1, 19, 14, 2, 5]
    #lst = []
    print(head(lst))

if __name__ == '__main__':
    main()