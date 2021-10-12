def main():
    x = int(input("X: "))
    y = int(input("Y: "))

    res = lambda x, y : abs(x) < abs(y)
    print(res(x, y))

if __name__ == "__main__":
    main()