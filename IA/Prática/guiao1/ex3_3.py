def convert(lst1, lst2):
    if len(lst1) != len(lst2):
        return None

    if lst1 == []:
        return []
    if lst2 == []:
        return []

    new_lst = [(lst1[0], lst2[0])] + convert(lst1[1:], lst2[1:])

    return new_lst

def main():
    lst1 = [1, 2, 3, 5, 6]
    lst2 = [7, 8, 9, 10, 11]
    new_lst = convert(lst1, lst2)
    print(new_lst)

if __name__ == "__main__":
    main()
