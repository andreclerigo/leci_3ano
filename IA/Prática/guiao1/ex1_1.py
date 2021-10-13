def getLength(lst):
    if lst == []:
        return 0

    size = 1 + getLength(lst[1:])

    return size

def main():
    lst = [1, 2, 3, 4, 5, -1]
    print(getLength(lst))

if __name__ == '__main__':
    main()
