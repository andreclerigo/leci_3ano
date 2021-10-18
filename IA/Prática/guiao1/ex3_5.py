def findMin(lst):
    if lst == []:
        return None
    
    if len(lst) == 1:
       return (lst[0], [])
    
    (m, l) = findMin(lst[1:])

    if lst[0] < m:
        return (lst[0], [m] + l)
    return (m, [lst[0]] + l)

def main():
    lst = [5, -2, 5, 2, 1, 19, 14, 2, 5]
    #lst = []
    print(findMin(lst))

if __name__ == '__main__':
    main()