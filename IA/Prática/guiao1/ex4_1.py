def main():
    n = int(input())

    res = lambda x : x % 2 == 0
    print(res(n))

if __name__ == "__main__":
    main()