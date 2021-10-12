import math

def main():
    x = int(input("X: "))
    y = int(input("Y: "))

    res = lambda x,y : (math.sqrt(x**2 + y**2), math.atan2(x, y))
    print(res(x, y))

if __name__ == "__main__":
    main()