def findMin(lst, func):
    if lst == []:
        return None
    
    if len(lst) == 2:
       return (lst[0], lst[1], [])
    
    (m1, m2, l) = findMin(lst[1:], func)

    if func(lst[0], m1):
        if func(m1, m2):
            return (lst[0], m1, [m2] + l)
        return (lst[0], m2, [m1] + l)

    if func(lst[0], m2):
        if func(m2, m1):
            return (lst[0], m2, [m1] + l)
        return (lst[0], m1, [m2] + l)

    return (m1, m2, [lst[0]] + l)

def main():
    lst = [5, -2, 5, 2, 1, 19, 14, 0, 0, 2, -2, 5]
    #lst = []
    func = lambda x, y: x < y
    print(findMin(lst, func))

if __name__ == '__main__':
    main()