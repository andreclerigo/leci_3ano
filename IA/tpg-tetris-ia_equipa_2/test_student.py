import os 
import sys
import time
from multiprocessing import Process


'''
How to run:

example: python3 test_student.py <num_of_runs> [random]
supress stdout: python3 test_student.py <num_of_runs> [random] > /dev/null 2>&1

if random is not specified, the number of runs can only be 10, 20, or 60
if random is chosen, the number of runs is up to you
'''


# generated using random.randint(0, 1000000)
SEEDS_10 = [536382, 575191, 100277, 158582, 577002, 520881, 240887, 819313, 336565, 229936]
SEEDS_20 = [656604, 378652, 752051, 66843, 233307, 274288, 467240, 953309, 14947, 854363, 
            741071, 263303, 1367, 338925, 493442, 174121, 143165, 657474, 530454, 412331]
SEEDS_60 = [835093, 122288, 642338, 703223, 105701, 210200, 128905, 215814, 111954, 800409, 223633, 171916, 21903, 988092, 
            495672, 744291, 69862, 907289, 451949, 415852, 941110, 506599, 64792, 694163, 20359, 715325, 284156, 523426, 
            407890, 206306, 380323, 834636, 998519, 377305, 690140, 787963, 519056, 329013, 35203, 947036, 772722, 268902, 
            925472, 255652, 457255, 726859, 71340, 431477, 7539, 663125, 563863, 235677, 127942, 128476, 539977, 713130, 
            427431, 729209, 40155, 477792]


def server(args):
    os.system(f"python3 server.py --seed {args}")

def viewer():
    os.system("python3 viewer.py")

def student():
    os.system("python3 student.py")

def main():
    if len(sys.argv) == 2:
        num_of_runs = int(sys.argv[1])
        r = False
    
    if len(sys.argv) == 3:
        num_of_runs = int(sys.argv[1])
        if sys.argv[2] == "random":
            r = True
        else:
            r = False

    if r:
        SEEDS = [0 for _ in range(num_of_runs)]
    else:
        if num_of_runs not in [10, 20, 60]:
            sys.exit("Invalid number of runs")

        if num_of_runs == 10:
            SEEDS = SEEDS_10
        if num_of_runs == 20:
            SEEDS = SEEDS_20
        if num_of_runs == 60:
            SEEDS = SEEDS_60

    for i in range(num_of_runs):
        seed = SEEDS[i]
        server_instance = Process(target=server, args=[seed,])
        viewer_instance = Process(target=viewer)
        student_instance = Process(target=student)
        
        server_instance.start()
        viewer_instance.start()
        time.sleep(1)
        student_instance.start()

        while True:
            if not student_instance.is_alive():
                server_instance.terminate()
                viewer_instance.terminate()
                student_instance.terminate()
                
                # clear the port
                os.system("fuser -k 8000/tcp")
                break


if __name__ == '__main__':
    main()
