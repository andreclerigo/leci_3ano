def conc_aplic(lst, func):
    if lst == []:
        return []

    if lst[0] == []:
        return conc_aplic(lst[1:], func)

    l = [func(lst[0][0])] + conc_aplic([lst[0][1:]] + lst[1:], func)

    return l

def main():
    lst = [[-2, 1, -3, 5], [2, -4, 10], [3, 4, 10], [0, -2, -5, 2], [-5, -3, -4], [1]]
    func = lambda x : x + 10
    print(conc_aplic(lst, func))

if __name__ == '__main__':
    main()
