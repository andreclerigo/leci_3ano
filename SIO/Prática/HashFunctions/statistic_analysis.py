import sys

def main():
    if len(sys.argv) != 3:
        print("Usage: python statistic_analysis.py <input_file1> <input_file2>")
        sys.exit(1)

    input_file1 = sys.argv[1]
    input_file2 = sys.argv[2]

    with open(input_file1, "rb") as f:
        data1 = f.read()

    with open(input_file2, 'rb') as f:
        data2 = f.read()

    bits = []

    for i in range(len(data1)):
        bits.append(bin(data1[i] ^ data2[i]))

    cnt = 0
    for bit in bits:
        for i in bit:
            if i == '1':
                cnt += 1

    print(f'Number of bits in file: {len(data1)*8}')
    print(f'Different bits: {cnt}')


if __name__ == '__main__':
    main()
    