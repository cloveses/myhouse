def reg(users):
    account = input('Please input your account:')
    passwd = input('Please input your password:')
    users[account] = passwd
    print('your account:', account)
    print('your password:', passwd)

def login(users):
    account = input('Please login account:')
    passwd = input('Please input password:')
    if account in users:
        if users[account] == passwd:
            print('login success!')
        else:
            print('password error!')
    else:
        print('account is not exist!')

def main():
    users = {}
    while True:
        print()
        print('1 [register]; 2 [login]; 0 [quit]')
        print('Please your command:')
        command = input()
        if command == '1':
            reg(users)
        elif command == '2':
            login(users)
        elif command == '0':
            break
        else:
            print('Bad command!')

if __name__ == '__main__':
    main()