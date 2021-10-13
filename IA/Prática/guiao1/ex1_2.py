def sum(lst):
    if lst == []:
        return 0

    s = lst[0] + sum(lst[1:])

    return s

def main():
    lst = [1, 2, 3, 4, 5, -1]
    print(sum(lst))

if __name__ == '__main__':
    main()
