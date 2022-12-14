import sqlite3
from random import randint
from sqlite3 import Error


def connect_db(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return conn

def create_table(conn):
    sql = """CREATE TABLE IF NOT EXISTS card (
                id integer PRIMARY KEY,
                number TEXT,
                pin TEXT,
                balance integer DEFAULT 0
            ); """
    try:
        c = conn.cursor()
        c.execute(sql)
    except Error as e:
        print(e)

def add_row(conn, row):
    sql = ''' INSERT INTO card(id,number,pin,balance)
                VALUES(?,?,?,?) '''
    cur = conn.cursor()
    cur.execute('select max(id) from card')
    id = cur.fetchone()
    id = 1 if id[0] is None else id[0] + 1
    val = [id] + row
    cur.execute(sql, val)
    conn.commit()

def select_all(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM card")
    rows = cur.fetchall()
    for row in rows:
        print(row)

class Card():
    cards = {}

    def __init__(self, num):
        if num in self.cards:
            self.num = num
            self.pin = self.cards[num][0]
            self.balance = self.cards[num][1]
        else:
            self.pin = self.get_pin()
            self.num = self.get_num()
            self.balance = 0

    def get_num(self):
        while True:
            n = randint(0, 999999999)
            if n not in [int(c[6:16]) for c in self.cards]:
                break
        c_num = '400000' + str(n).rjust(9, '0')
        c_num += chk_sum(c_num)
        self.cards[c_num] = (self.pin, 0)
        return c_num

    def get_pin(self):
        p = str(randint(0, 9999))
        return p.rjust(4, '0')

    def read_db(conn):
        cur = conn.cursor()
        cur.execute("SELECT * FROM card")
        rows = cur.fetchall()
        for row in rows:
            Card.cards[row[1]] = (row[2], row[3])


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
    row = [card.num, card.pin, card.balance]
    add_row(conn, row)
    print('Your card has been created')
    print(f'Your card number:\n{card.num}')
    print(f'Your card PIN:\n{card.pin}')

def log_in():
    cnum = input('Enter your card number:\n')
    pin = input('Enter your PIN:\n')
    if cnum in Card.cards and Card.cards[cnum][0] == pin:
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
            add_income(conn, card)
        elif cmd == '3':
            do_transfer(conn, card)
        elif cmd == '4':
            close_acc(conn, card)
            return True
        elif cmd == '5':
            print('You have successfully logged out!')
            return True
        else:
            return False

def update_balance(conn, card, sum):
    card.balance += sum
    sql = ''' UPDATE card
                SET balance = ?
                WHERE number = ?'''
    cur = conn.cursor()
    cur.execute(sql, (card.balance, card.num))
    conn.commit()

def del_card(conn, card):
    sql = '''DELETE FROM card WHERE number=?'''
    cur = conn.cursor()
    cur.execute(sql, (card.num,))
    conn.commit()

def add_income(conn, card):
    sum = int(input('Enter income:\n'))
    update_balance(conn, card, sum)
    print('Income was added!')

def do_transfer(conn, card):
    cn_to = input('Transfer\nEnter card number:\n')
    if cn_to[-1] != chk_sum(cn_to):
        print('Probably you made a mistake in the card number. Please try again!')
        return
    elif cn_to not in Card.cards:
        print('Such a card does not exist.')
        return
    else:
        sum = int(input('Enter how much money you want to transfer:\n'))
        print('sum=', sum, 'balance=', card.balance, sum < card.balance)
        if sum > card.balance:
            print('Not enough money!')
        else:
            card_to = Card(cn_to)
            update_balance(conn, card, -sum)
            update_balance(conn, card_to, sum)
            print('Success!')

def close_acc(conn, card):
    del_card(conn, card)
    print('The account has been closed!')

s_menu1 = '''
1. Create an account
2. Log into account
0. Exit
'''
s_menu2 = '''
1. Balance
2. Add income
3. Do transfer
4. Close account
5. Log out
0. Exit
'''

conn = connect_db('card.s3db')
create_table(conn)
Card.read_db(conn)
# select_all(conn)

loop = True
while loop:
    cmd = input(s_menu1)
    if cmd == '1':
        create_account()
    elif cmd == '2':
        loop = log_in()
    else:
        loop = False
print('\nBye!')

if conn:
    conn.close()
