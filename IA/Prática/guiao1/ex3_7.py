def remove(lst, n):
    if lst == []:
        return []

    if lst[0] != n:
        return [lst[0]] + remove(lst[1:], n)
    return remove(lst[1:], n)  

def findMin(lst):
    if lst == []:
        return None
    
    if len(lst) == 1:
       return lst[0]
    
    return min(lst[0], findMin(lst[1:]))

def createTriple(a, b, lst):
    if a is None:
        return None

    if b is None:
        return None
    
    return (a, b, lst)

def main():
    lst = [5, -2, 5, 2, 1, 19, 14, 2, 5]
    #lst = []
    #lst = [1]
    #lst = [1, 2]

    a = findMin(lst)
    lst = remove(lst, a)
    b = findMin(lst)
    lst = remove(lst, b)

    print( createTriple(a, b, lst) )

if __name__ == '__main__':
    main()