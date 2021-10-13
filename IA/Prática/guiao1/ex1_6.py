def reverse(lst):
    if lst == []:
        return []
    
    reverse_lst = reverse(lst[1:])

    reverse_lst[len(reverse_lst):] = [lst[0]]

    return reverse_lst

def capicua(lst):
    return reverse(lst) == lst
    
def main():
    lst = [1, 2, 3, 4, 3, 2, 1]
    #lst = [1, 2, 3]
    print(capicua(lst))

if __name__ == '__main__':
    main()
