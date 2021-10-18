def mergeLists(lst1, lst2, func):
    if lst1 == []:
        return []
    
    if lst2 == []:
        return []

    l = mergeLists(lst1[1:], lst2[1:], func)

    if func(lst1[0], lst2[0]):
        return [lst1[0]] + mergeLists(lst1[1:], lst2[:], func)
    return [lst2[0]] + mergeLists(lst1[:], lst2[1:], func)

def main():
    lst1 = [-5, -3, -1, 0, 0, 4, 5, 8]
    lst2 = [-3, 1, 1, 1, 5, 5, 5, 10]
    func = lambda x, y: x <= y
    print(mergeLists(lst1, lst2, func))

if __name__ == '__main__':
    main()