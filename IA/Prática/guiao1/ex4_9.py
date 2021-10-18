def findMin(lst, func):
    if lst == []:
        return None
    
    if len(lst) == 1:
       return lst[0]
    
    m = findMin(lst[1:], func)

    if func(lst[0], m):
        return lst[0]
    return m

def main():
    lst = [5, -2, 5, 2, 1, 19, 14, 2, 5]
    #lst = []
    func = lambda x, y: x < y
    print(findMin(lst, func))

if __name__ == '__main__':
    main()