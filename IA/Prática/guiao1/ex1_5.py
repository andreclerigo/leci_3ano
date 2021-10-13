def reverse(lst):
    if lst == []:
        return []
    
    reverse_lst = reverse(lst[1:])

    reverse_lst[len(reverse_lst):] = [lst[0]]

    return reverse_lst

def main():
    lst = [1, 2, 3, 4, 5, -1, -1]
    print(reverse(lst))

if __name__ == '__main__':
    main()
