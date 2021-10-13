def exist(lst, n):
    if lst == []:
        return False

    if lst[0] == n:
        return True
    
    return exist(lst[1:], n)

def main():
    lst = [1, 2, 3, 4, 5, -1, -1]
    n = int(input("Search: "))
    print(exist(lst, n))

if __name__ == '__main__':
    main()
