def findMax(lst):
    if lst == []:
        return None
    
    if len(lst) == 1:
       return lst[0]
    
    return max(lst[0], findMax(lst[1:]))

def findMin(lst):
    if lst == []:
        return None
    
    if len(lst) == 1:
       return lst[0]
    
    return min(lst[0], findMin(lst[1:]))

def createTup(a, b):
    if (a or b) == None:
        return None
    
    return (a, b)

def main():
    lst = [5, -2, 5, 2, 1, 19, 14, 2, 5]
    #lst = []

    print( createTup(findMin(lst), findMax(lst)) )

if __name__ == '__main__':
    main()