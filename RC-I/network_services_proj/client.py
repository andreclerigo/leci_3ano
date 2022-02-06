import socket
import signal
import sys
import os
import psutil
import time
import json
from reprint import output


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Global Variables
cpu_min = 100
cpu_max = 0
mem_min = 100
mem_max = 0
sock = None

# Signal Handler
def signal_handler(sig, frame):
    global sock

    info = json.loads(get_usage())
    info['done'] = True

    sock.send(json.dumps(info).encode())
    sock.close()
    os.system('clear')

    print(f"{bcolors.FAIL}\nConnection Closed!{bcolors.ENDC}")
    print(f"{bcolors.FAIL}Final Statistics\n{bcolors.ENDC}")
    sys.exit(0)

# Port Input Handler
def port_handler(port):
    # If the user chose default port, use 5005
    if port == "":
        port = 5005
    
    try:
        # Check if the input is a number
        port = int(port)

        # If the input is a number, check if its valid
        if port < 0 or port > 65535:
            raise ValueError

        return port
    except ValueError:
        print(f"{bcolors.FAIL}ERROR - Port used must be a number between 0-65535!{bcolors.ENDC}")
        sys.exit(0)

# Address Input Handler
def addr_handler(addr):
    # If the user chose default addr, use 127.0.0.1
    if addr == "" or addr == "localhost":
        return "127.0.0.1"

    # Parse the IP
    lst_octets = addr.split('.')

    # Check if the IP has the correct format
    if len(lst_octets) != 4:
        print(f"{bcolors.FAIL}ERROR - IP address must be in the form of xxx.xxx.xxx.xxx{bcolors.ENDC}")
        sys.exit(0)

    # Check if the octet is a number between 0-255
    for octet in lst_octets:
        try:
            octet = int(octet)

            if octet < 0 or octet > 255:
                raise ValueError
        except ValueError:
            print(f"{bcolors.FAIL}ERROR - Octet must be a number between 0-255{bcolors.ENDC}")
            sys.exit(0)
    
    return addr

# Delay Input Handler
def delay_handler(delay):
    # If the user chose default delay, use 1
    if delay == "":
        return 1
    
    try:
        # Check if the input is a number
        delay = int(delay)

        # If the input is a number, check if its valid
        if delay < 0:
            raise ValueError

        return delay
    except ValueError:
        print(f"{bcolors.FAIL}ERROR - Dealy used must be a positive number!{bcolors.ENDC}")
        sys.exit(0)

# Return a dictionary with the system information
def get_usage():
    global cpu_min, cpu_max, mem_min, mem_max

    # Get the current monitor values
    cpu_usage = psutil.cpu_percent()
    mem_usage = psutil.virtual_memory().percent

    # Update the min and max values
    if cpu_usage < cpu_min:
        cpu_min = cpu_usage
    
    if cpu_usage > cpu_max:
        cpu_max = cpu_usage

    if mem_usage < mem_min:
        mem_min = mem_usage

    if mem_usage > mem_max:
        mem_max = mem_usage

    # Create the progress bar string
    cpu_progress = "[" + "=" * int(cpu_usage//2) + " " * int(50 - (cpu_usage//2)) + "]"
    mem_progress = "[" + "=" * int(mem_usage//2) + " " * int(50 - (mem_usage//2)) + "]"

    return json.dumps({ 
        'cpu': cpu_progress , 
        'mem': mem_progress, 
        'cpu_min': cpu_min, 
        'cpu_curr': cpu_usage,
        'cpu_max': cpu_max, 
        'mem_min': mem_min, 
        'mem_curr': mem_usage,
        'mem_max': mem_max 
        })

def main():
    global sock

    # Intial Message to exit the program
    signal.signal(signal.SIGINT, signal_handler)
    print(f'{bcolors.WARNING}Press Ctrl+C to exit the program{bcolors.ENDC}')

    # Set the desired IP address
    addr = input(f"\n{bcolors.HEADER}{bcolors.BOLD}Choose IP to connect (default: 127.0.0.1): {bcolors.ENDC}")
    addr = addr_handler(addr)

    # Set the desired Port
    port = input(f"{bcolors.HEADER}{bcolors.BOLD}Choose port to connect (default: 5005): {bcolors.ENDC}")
    port = port_handler(port)

    # Set the desired delay
    delay = input(f"{bcolors.HEADER}{bcolors.BOLD}Choose delay between messages in seconds (default: 1): {bcolors.ENDC}")
    delay = delay_handler(delay)

    # Create a connection to the server
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((addr, port))

    print(f"{bcolors.OKGREEN}\nClient connected to {addr}:{port}\n{bcolors.ENDC}")    
    
    with output(output_type='dict') as output_lines:
        while True:
            try:
                info = get_usage()
                info_str = json.loads(info)

                output_lines[f' {bcolors.OKBLUE}MEM'] = "{}".format(info_str['mem'])
                output_lines[f' {bcolors.OKBLUE}MEM Info \t Max'] = "{}%\tMin: {}%\tCurrent: {}%".format(info_str['mem_max'], info_str['mem_min'], info_str['mem_curr'])
                output_lines[f' {bcolors.OKCYAN}CPU'] = "{}".format(info_str['cpu'])
                output_lines[f' {bcolors.OKCYAN}CPU Info \t Max'] = "{}%\tMin: {}%\tCurrent: {}%".format(info_str['cpu_max'], info_str['cpu_min'], info_str['cpu_curr'])

                sock.send(info.encode())
                time.sleep(delay)
            except (socket.timeout, socket.error):
                os.system('clear')
                print(f"{bcolors.FAIL}Server error. Done!{bcolors.ENDC}")
                print(f"{bcolors.FAIL}Final Statistics\n{bcolors.ENDC}")
                sys.exit(0)

if __name__ == '__main__':
    main()
