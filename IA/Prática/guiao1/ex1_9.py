def union(lst1, lst2):
    if lst1 == []:
        return lst2
    if lst2 == []:
        return lst1
    
    union_lst = []

    if lst2[0] < lst1[0]:
        union_lst[:0] = [lst2[0]]
        return union_lst + union(lst1, lst2[1:])
    
    if lst1[0] < lst2[0]:
        union_lst[:0] = [lst1[0]]
        return union_lst + union(lst1[1:], lst2)
    
    union_lst[:0] = [lst1[0], lst2[0]]
    return union_lst + union(lst1[1:], lst2[1:])

def main():
    lst1 = [1, 2, 2, 3, 5, 8, 20]
    lst2 = [0, 2, 4, 5, 10, 12]
    new_lst = union(lst1, lst2)
    print(new_lst)

if __name__ == "__main__":
    main()