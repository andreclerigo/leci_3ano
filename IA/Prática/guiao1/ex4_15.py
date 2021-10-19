def aplic_combin(tup, func):
    if tup == []:
        return []

    if tup[0] == []:
        return aplic_combin(tup[1:], func)

    l = [func(tup[0][0])] + aplic_combin([tup[0][1:]] + list(tup[1:]), func)

    return l

def main():
    tup = ([-2, 1, -3, 5], [2, -4, 10], [3, 4, 10], [0, -2, -5, 2], [-5, -3, -4], [1])
    func = lambda x : x > 0
    print(aplic_combin(tup, func))

if __name__ == '__main__':
    main()
    