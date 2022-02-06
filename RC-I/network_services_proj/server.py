import socket
import selectors
import signal
import sys
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

# Create a selector for multiple clients
sel = selectors.DefaultSelector()

# Signal Handler
def signal_handler(sig, frame):
    print(f"{bcolors.FAIL}\nConnection Closed!{bcolors.ENDC}")
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

# Max Backlog Connections Input Handler
def max_backlog_conns_handler(max_backlog_conns):
    # If the user chose default max_backlog_conns, use 10
    if max_backlog_conns == "":
        return 10
    
    try:
        # Check if the input is a number
        max_backlog_conns = int(max_backlog_conns)

        # If the input is a number, check if its valid
        if max_backlog_conns < 0:
            raise ValueError

        return max_backlog_conns
    except ValueError:
        print(f"{bcolors.FAIL}ERROR - Number of clients must be a positive number!{bcolors.ENDC}")
        sys.exit(0)

# Acept the client connection
def handle_client_connection(server_socket):   
    client_socket, address = server_socket.accept()
    print(f"{bcolors.OKGREEN}Accepted connection from {address[0]}:{address[1]}{bcolors.ENDC}")
    client_socket.setblocking(False)
    sel.register(client_socket, selectors.EVENT_READ, handle_data)

# Handle the data sent by the client
def handle_data(client_socket):
    global print_format

    address = client_socket.getpeername()
    address = str(address[0]) + ":" + str(address[1])
    try:
        request = client_socket.recv(1024)
        if not request:
            sel.unregister(client_socket)
            client_socket.close()
        else:
            msg = request.decode()
            formatted_print(msg, address)
    except (socket.timeout,socket.error):
        print(f"{bcolors.FAIL}Client {address} error. Done!{bcolors.ENDC}")

# Print the systems information
def formatted_print(info, raddr):
    info = json.loads(info)

    if 'done' in info:
        print(f"{bcolors.WARNING}Client {raddr} disconnected!{bcolors.ENDC}")
        print(f"{bcolors.WARNING}Max CPU Usage: {info['cpu_max']}% - Min CPU Usage: {info['cpu_min']}%{bcolors.ENDC}")
        print(f"{bcolors.WARNING}Max MEM Usage: {info['mem_max']}% - Min MEM Usage: {info['mem_min']}%{bcolors.ENDC}\n")
    else:
        x = info["cpu_curr"]
        y = info["mem_curr"]

        print(f"{bcolors.OKBLUE}Received from {raddr} - CPU: {x}% - MEM: {y}%{bcolors.ENDC}")
    
def main():
    # Intial Message to exit the program
    signal.signal(signal.SIGINT, signal_handler)
    print(f'{bcolors.WARNING}Press Ctrl+C to exit the program{bcolors.ENDC}')

    addr = "0.0.0.0"

    # Set the desired Port
    port = input(f"{bcolors.HEADER}{bcolors.BOLD}Choose port to list (default: 5005): {bcolors.ENDC}")
    port = port_handler(port)

    # Set the desired number of max connections
    max_backlog_conns = input(f"{bcolors.HEADER}{bcolors.BOLD}Choose max backlog connections (default: 10): {bcolors.ENDC}")
    max_backlog_conns = max_backlog_conns_handler(max_backlog_conns)

    # Create Server Socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((addr, port))

    # Set the max connections to the server
    server.listen(max_backlog_conns)
    server.setblocking(False) 
    sel.register(server, selectors.EVENT_READ, handle_client_connection)

    print(f'\n{bcolors.OKGREEN}Server running on {addr}:{port}{bcolors.ENDC}')
    print(f'{bcolors.OKGREEN}Max backlog connections: {max_backlog_conns}\n{bcolors.ENDC}')

    while True:
        events = sel.select()
        for key, mask in events:
            callback = key.data
            selsocket = key.fileobj
            callback(selsocket)

if __name__ == '__main__':
    main()
