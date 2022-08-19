from random import randint

class Card():
    cards = {}

    def __init__(self, num):
        if num in self.cards:
            self.num = num
            self.pin = self.cards[num]
        else:
            self.pin = self.get_pin()
            self.num = self.get_num()
        self.balance = 0

    def get_balance(self):
        return self.balance

    def get_num(self):
        while True:
            n = randint(0, 999999999)
            if n not in [int(c[6:16]) for c in self.cards]:
                break
        c_num = '400000' + str(n).rjust(9, '0')
        c_num += chk_sum(c_num)
        self.cards[c_num] = self.pin
        return c_num

    def get_pin(self):
        p = str(randint(0, 9999))
        return p.rjust(4, '0')


def chk_sum(num):
    sum = 0
    for i in range(0, 15):
        if i % 2 == 0:
            n = int(num[i]) * 2
            sum += n if n < 9 else n - 9
        else:
            sum += int(num[i])
    return str((10 - sum % 10) % 10)

def create_account():
    card = Card('')
    print('Your card has been created')
    print(f'Your card number:\n{card.num}')
    print(f'Your card PIN:\n{card.pin}')

def log_in():
    cnum = input('Enter your card number:\n')
    pin = input('Enter your PIN:\n')
    if cnum in Card.cards and Card.cards[cnum] == pin:
        card = Card(cnum)
        print('\nYou have successfully logged in!')
    else:
        print('\nWrong card number or PIN!')
        return True

    while True:
        cmd = input(s_menu2)
        if cmd == '1':
            print(f'Balance: {card.balance}')
        elif cmd == '2':
            print('You have successfully logged out!')
            return True
        else:
            return False


s_menu1 = '''
1. Create an account
2. Log into account
0. Exit
'''
s_menu2 = '''
1. Balance
2. Log out
0. Exit
'''

loop = True
card = ''

while loop:
    cmd = input(s_menu1)
    if cmd == '1':
        create_account()
    elif cmd == '2':
        loop = log_in()
    else:
        loop = False
print('\nBye!')
