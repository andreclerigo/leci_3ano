def convert(lst, index):
    if lst == []:
        return []

    new_lst = [lst[0][index]] + convert(lst[1:], index)

    return new_lst

def main():
    lot = [(1, 2), (0, 9), (10, 2), (5, 6), (8, 1)]
    tol = (convert(lot, index=0), convert(lot, index=1))
    print(tol)

if __name__ == "__main__":
    main()