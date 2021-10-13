def contagem(lst, n):
    if lst == []:
        return 0

    if lst[0] == n:
        return 1 + contagem(lst[1:], n) 
    return contagem(lst[1:], n)

def main():
    lst = [-20, 5, -2, 5, 2, 1, 19, 14, 2, 5]
    for n in lst:
        print((n, contagem(lst, n)))

if __name__ == '__main__':
    main()