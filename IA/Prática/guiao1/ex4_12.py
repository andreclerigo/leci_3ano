import math

def main():
    x = int(input("X: "))
    y = int(input("Y: "))

    #res = lambda x,y : (math.sqrt(x**2 + y**2), math.atan2(x, y))
    #print(res(x, y))
    lst = (x, y)

    for (a,b) in lst:
        print(a)
        print(b)

    n = [math.sqrt(n**2 + n**2) for n in lst]
    print(n)

if __name__ == "__main__":
    main()