from glitter import exploits

BOUNTY_END_ACTION = 11

EXPLOIT_MENU = """\033[92m[SWISSKNIFE]:\033[0m Please choose an exploit:
                  [1] - Like Exploit (Add More Likes)
                  [2] - Color Glit Exploit (Add Custom Colored background for a glit (Not Standard))
                  [3] - Force Friend Request (Add any friend you would want!)
                  [4] - Comment on private glit (Can be used for normal once too but intended for private glit id)
                  [5] - Show Unintended Data from search (Get users data!)
                  [6] - Show privates users feed from name (Can be used for normal once too but intended for private accounts)
                  
                  [BOUNTIES]:
                  [7] - Login to any account from name (Only for demonstration purposes cant do actions on it)
                  [8] - Get any accounts password from name
                  [9] - Get any accounts cookie ID (Identifier for the account when logged in)
                  [10] - Get any accounts search history (Glitter search :P)
                  [11] - Send Malicious glit to a feed of choice (feed -> profile)"""

INPUT_MENU = {
    'username': '\033[93mEnter username:\033[0m ',
    'password': '\033[93mEnter password:\033[0m ',
    'glit_id': '\033[93mEnter ID of a Glit:\033[0m ',
    'content': '\033[93mEnter content of the Glit:\033[0m ',
    'color': '\033[93mEnter background color for Glit:\033[0m ',
    'feed_name': '\033[93mEnter name of the profile that you want to glit too (send nothing for this profile):\033[0m ',
    'friend_name': '\033[93mEnter name of friend that you want to friends with:\033[0m ',
    'priv_glit_id': '\033[93mEnter ID of a Private Glit (can be found with show private feed):\033[0m ',
    'private_name': '\033[93mEnter name of the private profile that you want to see its feed:\033[0m ',
    'search_term': '\033[93mEnter search term:\033[0m ',
}


def main():
    print('\033[92m[SWISSKNIFE]:\033[0m Welcome to the exploit program please login to your glitter account:')
    try:
        username = str(input(INPUT_MENU['username']))
        password = str(input(INPUT_MENU['password']))

        account = exploits(username, password)
    except Exception as err:
        print(f'\033[91m[ERROR]:\033[0m {err}')
        return None

    try:
        while True:
            try:
                # Act apon menu:
                print(EXPLOIT_MENU)
                try:
                    choice = int(input('Please make your choice: '))
                    if choice < 1 or choice > BOUNTY_END_ACTION:
                            raise ValueError('Invalid choice')
                except ValueError or TypeError:
                    print(f'\033[92m[WARNING]:\033[0m Invalid input, please try again.')
                    # As an invalid input was catched try getting the input again.
                    continue

                if choice == 1:
                    try:
                        glit_id = int(input(INPUT_MENU['glit_id']))
                    except TypeError:
                        print(f'\033[92m[WARNING]:\033[0m Invalid input, please try again.')
                        # As an invalid input was catched try getting the input again.
                        continue
                    account.like_exploit(glit_id)
                    continue # We have finished our choice action and we move on to the next one.

                if choice == 2:
                    try:
                        feed_name = str(input(INPUT_MENU['feed_name']))
                        if feed_name == '':
                            feed_name = None

                        color = str(input(INPUT_MENU['color']))
                        content = str(input(INPUT_MENU['content']))
                    except TypeError:
                        print(f'\033[93m[WARNING]:\033[0m Invalid input, please try again.')
                        # As an invalid input was catched try getting the input again.
                        continue
                    account.custom_color_exploit(content, color, feed_name)
                    continue # We have finished our choice action and we move on to the next one.

                if choice == 3:
                    try:
                        friend_name = str(input(INPUT_MENU['friend_name']))
                    except TypeError:
                        print(f'\033[93m[WARNING]:\033[0m Invalid input, please try again.')
                        # As an invalid input was catched try getting the input again.
                        continue
                    account.force_friend_exploit(friend_name)   
                    continue # We have finished our choice action and we move on to the next one.

                if choice == 4:
                    try:
                        glit_id = int(input(INPUT_MENU['priv_glit_id']))
                        content = str(input(INPUT_MENU['content']))
                    except TypeError:
                        print(f'\033[93m[WARNING]:\033[0m Invalid input, please try again.')
                        # As an invalid input was catched try getting the input again.
                        continue
                    account.comment_priv_glit_exploit(glit_id, content)
                    continue # We have finished our choice action and we move on to the next one.

                if choice == 5:
                    try:
                        term = str(input(INPUT_MENU['search_term']))
                    except TypeError:
                        print(f'\033[93m[WARNING]:\033[0m Invalid input, please try again.')
                        # As an invalid input was catched try getting the input again.
                        continue
                    account.search_exploit(term)
                    continue # We have finished our choice action and we move on to the next one.

                if choice == 6:
                    try:
                        private_name = str(input(INPUT_MENU['private_name']))
                    except TypeError:
                        print(f'\033[93m[WARNING]:\033[0m Invalid input, please try again.')
                        # As an invalid input was catched try getting the input again.
                        continue
                    account.view_priv_feed_exploit(private_name)
                    continue # We have finished our choice action and we move on to the next one.

                if choice == 7:
                    try:
                        user_name = str(input(INPUT_MENU['username']))
                    except TypeError:
                        print(f'\033[93m[WARNING]:\033[0m Invalid input, please try again.')
                        # As an invalid input was catched try getting the input again.
                        continue
                    account.login_without_pass_bug(user_name)
                    continue # We have finished our choice action and we move on to the next one.

                if choice == 8:
                    try:
                        user_name = str(input(INPUT_MENU['username']))
                    except TypeError:
                        print(f'\033[93m[WARNING]:\033[0m Invalid input, please try again.')
                        # As an invalid input was catched try getting the input again.
                        continue
                    account.get_password_bug(user_name)
                    continue # We have finished our choice action and we move on to the next one.

                if choice == 9:
                    try:
                        user_name = str(input(INPUT_MENU['username']))
                    except TypeError:
                        print(f'\033[93m[WARNING]:\033[0m Invalid input, please try again.')
                        # As an invalid input was catched try getting the input again.
                        continue
                    print(account.getUserSparkle(user_name))
                    continue # We have finished our choice action and we move on to the next one.                

                if choice == 10:
                    try:
                        user_name = str(input(INPUT_MENU['username']))
                    except TypeError:
                        print(f'\033[93m[WARNING]:\033[0m Invalid input, please try again.')
                        # As an invalid input was catched try getting the input again.
                        continue
                    account.get_user_history_bug(user_name)
                    continue # We have finished our choice action and we move on to the next one.

                if choice == 11:
                    try:
                        feed_name = str(input(INPUT_MENU['feed_name']))
                        if feed_name == '':
                            feed_name = None
                    except TypeError:
                        print(f'\033[93m[WARNING]:\033[0m Invalid input, please try again.')
                        # As an invalid input was catched try getting the input again.
                        continue
                    account.xsrf_xss_bug(feed_name)


            except Exception as err:
                print(f'\033[91m[ERROR]:\033[0m {err}')
    except KeyboardInterrupt:
            print('\033[93m[DISCONNECTED]:\033[0m Bye Bye!')
            del account
    
        
if __name__ == '__main__':
    try:
        main()
    except Exception:
        print('\033[91m[CRITICAL ERROR]:\033[0m Bye Bye!')