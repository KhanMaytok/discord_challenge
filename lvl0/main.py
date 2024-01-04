import json

file_path = './db.json'


def save(json_object):
    with open(file_path, 'w') as f:
        json.dump(json_object, f)


def load():
    with open(file_path, 'r') as f:
        return json.load(f)


def find_user_id(username):
    for idx, user in enumerate(load()['users']):
        if user['username'] == username:
            return idx
    return -1


def options_validator(end):
    has_errors = True
    while has_errors is True:
        try:
            option = input()
            parsed_option = int(option)
            rg = range(0, end + 1)
            test = rg[parsed_option - 1]
            has_errors = False
            return parsed_option
        except ValueError:
            print("Please enter a number")
            continue
        except IndexError:
            print("Please enter a listed option")


def input_a_number(message):
    has_errors = True
    while has_errors is True:
        print(message)
        try:
            number = int(input())
            return number
        except ValueError:
            continue


def init():
    # Init the file every start up.
    data = {
        'users': [
            {'username': 'user1', 'password': 'password1', 'balance': 2000},
            {'username': 'user2', 'password': 'password2', 'balance': 2000},
            {'username': 'user3', 'password': 'password3', 'balance': 2000},
        ]
    }
    with open(file_path, 'w') as f:
        json.dump(data, f)


def login():
    username = input("Username:")
    password = input("Password:")
    with open(file_path, 'r') as f:
        data = json.load(f)
        users = data.get('users', [])
        # return any(user['username'] == username and user['password'] == password for user in users)
        for index, user in enumerate(users):
            if user['username'] == username and user['password'] == password:
                return True, index
        return False, None


def lock_login(times):
    attempts = 0
    is_logged = False
    index = None
    while attempts < times and is_logged is False:
        is_logged, index = login()
        if is_logged:
            continue
        attempts = attempts + 1
        print(f'Bad user or password. You have {times - attempts} attempts remaining')
    if is_logged is False:
        raise Exception('Login attempts exceeded. Please locate a bonfire and rest')
    return is_logged, index


def print_assessments_menu():
    print('1. Online banking system')
    print('2. Currency converter')
    print('3. University enrollment')
    print('4. Online shipping system')
    print('5. Finance management application')
    print('0. Exit\n')


def welcome():
    init()
    print(f'Welcome to the Spaghetti Inc.')
    option = ""
    while input != 0:
        print('Please select an option')
        print_assessments_menu()
        option = options_validator(5)
        match option:
            case 1:
                assessment_1()
            case 2:
                print('Not implemented')
            case 3:
                print('Not implemented')
            case 4:
                print('Not implemented')
            case 5:
                print('Not implemented')
            case 0:
                print('Bye!')
                break


def assessment_1():
    def display_option_menu():
        print('Please choose an option:\n')
        print('1. Deposit')
        print('2. Withdraw')
        print('3. View')
        print('4. Transfer')
        print('0. Exit\n')

    print('Welcome to the online banking system. Please enter your credentials.\n')
    is_logged, user_id = lock_login(3)

    option = ""
    while option != 0:
        display_option_menu()
        option = options_validator(4)
        match option:
            case 1:
                deposit = input_a_number("Please enter the amount to deposit:")
                print(
                    f'Ok, you have deposited {deposit} solaris in your account. We havn\'t shown any confirmation message because this system is not for cowards.')
                jo = load()
                balance = jo['users'][user_id]['balance']
                balance = balance + deposit
                jo['users'][user_id]['balance'] = balance
                print(f'You now have {balance} solaris in your account.')
                save(jo)
            case 2:
                withdraw = input_a_number("Please enter the amount to withdraw:")
                jo = load()
                balance = jo['users'][user_id]['balance']
                if withdraw > balance:
                    print(f'Hey buddy, you don\'t have that much money')
                else:
                    balance = balance - withdraw
                    jo['users'][user_id]['balance'] = balance
                    save(jo)
                    print(f'{withdraw} were withdrawn. You now have {balance} solaris')
            case 3:
                jo = load()
                balance = jo['users'][user_id]['balance']
                print(f'Hey buddy, you have {balance} solaris')
            case 4:
                transfer = input_a_number("Please enter the amount to transfer")
                username = input('Please enter the user who would like to transfer (username like user1, user2, user3)')
                jo = load()
                balance = jo['users'][user_id]['balance']
                if transfer > balance:
                    print(f'Hey buddy, you don\'t have that much money')
                else:
                    target_id = find_user_id(username)
                    if target_id == -1:
                        print('Sorry, we dont have that user')
                        continue
                    if target_id == user_id:
                        print('Self-transfer? No No No No')
                        continue
                    target_balance = jo['users'][target_id]['balance']
                    target_balance = target_balance + transfer
                    balance = balance - transfer
                    jo['users'][target_id]['balance'] = target_balance
                    jo['users'][user_id]['balance'] = balance
                    save(jo)
                    print(f'{transfer} were transfered. You now have {balance} solaris')


if __name__ == '__main__':
    welcome()
