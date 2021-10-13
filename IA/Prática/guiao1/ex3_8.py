def avg(lst):
    if lst == []:
        return 0
    
    r = lst[0] + avg(lst[1:])

    return r

def tup(avg, lst):
    if lst == []:
        return None
    
    return (avg, lst[len(lst)//2 - 1])

def main():
    lst = [-5, -2, -1, 0, 1, 1, 1, 4, 7, 8, 10]
    #lst = []
    print(tup(avg(lst), lst))

if __name__ == '__main__':
    main()