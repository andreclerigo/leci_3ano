def findMin(lst):
    if lst == []:
        return None
    
    if len(lst) == 1:
       return lst[0]
    
    return min(lst[0], findMin(lst[1:]))

def main():
    lst = [5, -2, 5, 2, 1, 19, 14, 2, 5]
    #lst = []
    print(findMin(lst))

if __name__ == '__main__':
    main()