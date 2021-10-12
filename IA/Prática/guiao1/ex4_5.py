def f(x, y):
    return x + y

def g(y, z):
    return y - z

def h(x, y):
    return x * y

def F(x, y, z):
    r = lambda x, y, z : h(f(x, y), g(y, z))
    return r(x, y, z)

def main():
    x = int(input("X: "))
    y = int(input("Y: "))
    z = int(input("Z: "))

    res = lambda x, y, z: F(x, y, z)
    print(res(x, y, z))

if __name__ == "__main__":
    main()