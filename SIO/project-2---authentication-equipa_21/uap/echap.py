import hashlib
import socket
import sqlite3
import struct
import random
import random
import string
import sqlite3
import os
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from base64 import b64encode, b64decode
import random


# Constants used in the protocol fields
AUTH_REQUEST_CODE = 0x00
CHALLENGE_CODE = 0x01
RESPONSE_CODE = 0x02
SUCCESS_CODE = 0x03
FAILURE_CODE = 0x04

# Code (1 byte) + Identifier (1 byte) + Length (2 bytes)
header_len = 4


# Receives a packet from a connection and returns a formatted dictionary
def receive_packet(conn):
    # Receives package
	packet = conn.recv(header_len)
	if packet == '':
		raise RuntimeError("Connection Stopped Unexpectedly")

    # Unpacks the packet
	code, identifier, length = struct.unpack('!BBH', packet)

	while len(packet) < length:
		chunk = conn.recv(length - len(packet))
		if chunk == '':
			raise RuntimeError("Connection Stopped Unexpectedly")
		packet = packet + chunk

    # Returns the packet structure
	code, identifier, length, data = struct.unpack('!BBH' + str(length - header_len) + 's', packet)
	return {'code' : code,
            'identifier' : identifier,
            'length' : length,
            'data' : data }

# Creates a packet with the given code, identifier and data, ready to be sent
def create_protocol_packet(code, identifier, data):
    data_len = len(data)
    packet_len = header_len + data_len

    # Packing format:
    # ! - use network byte order
    # B - encode as a C unsigned char (1 byte)
    # s - encode as a string character

    pack_format = '!BBH' + str(data_len) + 's'
    packet = struct.pack(pack_format, code, identifier, packet_len, data)

    return packet

# Generates a Challenge packet with the Challenge value and Salt used to hash the password
def create_challenge(config, salt):
    # Creates challenge identifier
    identifier = random.randint(0, 255)

    # Creates random challenge
    challenge_value = os.urandom(32)
    challenge_value_size = struct.pack('!B', len(challenge_value))
    salt_size = struct.pack('!B', len(salt))
    name = config['localname']

    data = challenge_value_size + challenge_value + salt_size + salt + name

    # Creates Challenge package
    packet = create_protocol_packet(CHALLENGE_CODE, identifier, data)
    
    print("Creating challenge with identifier:", identifier)
    return packet, identifier, challenge_value

# Returns True or False wheter the response received is correct or not
def verify_bit_response(response_packet, identity, identifier, bit_position, expected_key):
    # Verify if the packet is a response
    if response_packet['code'] != RESPONSE_CODE:
        print("Response packet is not a response packet")
        return False

    # Get the data len from the first byte of the packet
    data_len = response_packet['data'][0]
    # Converts data bytes to integer
    data_value = int.from_bytes(response_packet['data'][1:data_len+1], 'big')
    # The rest of the data is the name
    name = response_packet['data'][data_len+1:]

    # Verify if the name on the packet matches the expect identity
    if name == identity:
        # Verify if the identifier on the packet matches the expect identifier
        if response_packet['identifier'] == identifier:
            expected_value = expected_key[bit_position//8] >> (bit_position%8) & 0x01

            if expected_value == data_value:
                return True 
            print("Response value does not match the expected value")
            return False
        else:
            print("Response identifier does not match expected identifier")
            return False
    else:
        print("Response identity does not match expected identity!")
        return False

# Starts the authenticator process
def authenticator(db_path):
    while True:
        # Config authenticator
        config = {}
        config['port'] = '5005'
        config['localname'] = b'localhost'

        # Create a socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('', int(config['port'])))  # Host == '' means any local IP address
        print("Waiting for incoming authentication requests...")
        sock.listen()
        conn, addr = sock.accept()

        # Receive the request for authentication
        packet = receive_packet(conn)

        # Check if the connection has the itent of authentication
        if (packet['code'] == AUTH_REQUEST_CODE):
            # Parse the authentication request
            user_size = packet['data'][0]
            user = packet['data'][1 : user_size+1]
            identity_size = packet['data'][user_size+1]
            identity = packet['data'][user_size+2 :user_size+2+identity_size]

            # Connects to the database 
            with sqlite3.connect(db_path) as db:
                res = db.execute('SELECT * FROM users WHERE username="%s"' % user.decode('utf-8'))
            data = res.fetchall()

            # Fetches the user's salt and hashed password
            try:
                salt = b64decode(data[0][5])
                hashed_pw = data[0][4]
            except:
                # If the user doesn't exist, send random data
                salt = os.urandom(32)
                hashed_pw = ''.join(random.choice(string.ascii_letters) for i in range(10)) 

            # Creates the Challenge package
            packet, challenge_identifier, challenge = create_challenge(config, salt)
            # Send the challenge
            conn.sendall(packet)

            # Expected key
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=challenge,
                iterations=100000,
            )
            key = kdf.derive(hashed_pw.encode())

            flag = True     # Flag error on packet received
            # Send the key bit by bit to the authenticator (128 bits chagend, 64 sent)
            for n in range(0, 128, 2):
                # Receive the response
                packet = receive_packet(conn)

                # If an error was detected, no more verification is needed
                if flag:
                    # Check if the packet is corret
                    res = verify_bit_response(packet, identity, challenge_identifier, n, key)
                    # Get the n bit from the key
                    value = (key[(n+1)//8] >> ((n+1) % 8) & 0x01).to_bytes(1, byteorder='big')
                    if flag and not res:
                        flag = False
                else:
                    # If an error was dectected generate random bit value
                    value = random.randint(0, 1).to_bytes(1, byteorder='big')

                value_size = struct.pack('!B', len(value))
                name = config['localname']
                data = value_size + value + name

                # Create the response packet
                packet = create_protocol_packet(RESPONSE_CODE, packet['identifier'], data)
                # Send the response
                conn.sendall(packet)

            # After the process is finished, send either a success or failure
            if flag:
                code = SUCCESS_CODE
                # Create a random token used for authentication
                data = os.urandom(32)

                kdf = PBKDF2HMAC(
                    algorithm=hashes.SHA256(),
                    length=32,
                    salt=data,
                    iterations=100000,
                )
                token = kdf.derive(hashed_pw.encode())

                with sqlite3.connect(db_path) as db:
                    db.execute('UPDATE users SET auth_token="%s" WHERE username="%s"' % (b64encode(token).decode('utf-8'), user.decode('utf-8')))
                    db.commit()
            else:
                code = FAILURE_CODE
                data = b'Identity or secret is incorrect'

            # Creates protocol package with SUCCESS or FAILURE code
            packet = create_protocol_packet(code, challenge_identifier, data)

            # Sends final package of protocol
            conn.sendall(packet)
            sock.close()
        else:
            sock.close()
            print("Packet is not an authentication request")

# Begins the authentication process and returns (True, auth_token) or (False, bit_failed)
def peer(username, password):
    # Config peer
    config = {}
    config['authenticator'] = "127.0.0.1"
    config['port'] = 5005
    config['identity'] = username.encode()
    config['secret'] = password.encode()
    config['localname'] = b"UAP"

    # Create socket to connect to the authenticator
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((config['authenticator'], config['port']))

    # Create the authentication request packet
    identity_size = struct.pack('!B', len(config['identity']))
    name_size = struct.pack('!B', len(config['localname']))
    # Request consist of the username and the localname
    data = identity_size + config['identity'] + name_size + config['localname']
    packet = create_protocol_packet(AUTH_REQUEST_CODE, 0x00, data)

    # Send the authentication request
    sock.sendall(packet)

    # Receive the challenge
    packet = receive_packet(sock)
    
    # Check the packet is a Challenge
    if (packet['code'] == CHALLENGE_CODE):
        # Parse the challenge packet
        challenge_len = packet['data'][0]
        challenge = packet['data'][1 : challenge_len+1]
        salt_len = packet['data'][challenge_len+1]
        salt = packet['data'][challenge_len+2 : challenge_len+salt_len+2]
        name =  packet['data'][challenge_len+salt_len+2 : ]

        print("Processing challenge with identifier:", packet['identifier'], "name:", name)
        challenge_data =  {'identifier' : packet['identifier'],
                            'challenge' : challenge,
                            'salt' : salt,
                            'name' : name }

        # Expected key
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=challenge_data['challenge'],
            iterations=100000,
        )
        hashed_pw = hashlib.sha256(config['secret'] + salt).hexdigest()
        key = kdf.derive(hashed_pw.encode())

        flag = True     # Flag error on packet received
        fail = None     # Get the bit where the error occured

        # Send the key bit by bit to the authenticator (128 bits chagend, 64 sent)
        for n in range(0, 128, 2):
            # If the flag is true, the packet is correct
            if flag:
                # Get the n bit from the key
                value = (key[n//8] >> (n % 8) & 0x01).to_bytes(1, byteorder='big')
            else:
                # If an error was dectected generate random bit value
                value = random.randint(0, 1).to_bytes(1, byteorder='big')

            value_size = struct.pack('!B', len(value))
            name = config['localname']
            data = value_size + value + name

            # Create the response packet
            packet = create_protocol_packet(RESPONSE_CODE, challenge_data['identifier'], data)
            # Send the response
            sock.sendall(packet)

            # Receive the response (challenge)
            packet = receive_packet(sock)

            # If an error was detected, no more verification is needed
            if flag:
                # Check if the packet is corret
                res = verify_bit_response(packet, challenge_data['name'], challenge_data['identifier'], n+1, key)
                if flag and not res:
                    flag = False
                    fail = n+1      # Get the bit were the error occured

        # Receive the authenticationtoken
        packet = receive_packet(sock)
        if (packet['code'] == SUCCESS_CODE):
            print("Success!")
            sock.close()

            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=packet['data'],
                iterations=100000,
            )
            token = kdf.derive(hashed_pw.encode())

            return True, b64encode(token).decode('utf-8')
        elif ((packet['code'] == FAILURE_CODE)):
            print("Failed!")
            sock.close()
            return False, fail
    else:
        print("Packet is not an authentication request")
        sock.close()
        return False, ''
