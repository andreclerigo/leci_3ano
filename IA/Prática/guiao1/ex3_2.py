def tail(lst):
    if lst == []:
        return None

    return lst[-1]

def main():
    lst = [-20, 5, -2, 5, 2, 1, 19, 14, 2, 5]
    #lst = []
    print(tail(lst))

if __name__ == '__main__':
    main()