def getOrder(lst):
    if len(lst) < 1:
        return None
    
    if len(lst) == 1:
        return (lst[0], [])
    
    if lst[0] < lst[1]:
        return (lst[0], lst[1:])

    if lst[1] < lst[0]:
        return (lst[-1], lst[:-1])


def main():
    #lst = []
    #lst = [1]
    lst = [1, 2, 3, 4, 5, 6, 7]
    #lst = [4, 3, 2, 1]
    print(getOrder(lst))

if __name__ == "__main__":
    main()