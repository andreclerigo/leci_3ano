def substituir(lst, x, y):
    if lst == []:
        return []
    
    sub_lst = substituir(lst[1:], x, y)
    if lst[0] == x:
        return [y] + sub_lst
    return [lst[0]] + sub_lst

def main():
    lst = [1, 2, 2, 4, 5, 2, 1, 7, 8]
    x = int(input("Insira o x: "))
    y = int(input("Insira o y: "))
    new_lst = substituir(lst, x, y)
    print(new_lst)

if __name__ == "__main__":
    main()