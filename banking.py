# Re-design inspired by zetta ^_^

from random import sample
import sqlite3


class Banking:
    def __init__(self):
        self.credit_card = None
        self.pin = None
        self.conn = sqlite3.connect('card.s3db')
        self.cur = self.conn.cursor()
        self.sql_table()

    def sql_table(self):
        query = """CREATE TABLE IF NOT EXISTS card (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 
                number TEXT NOT NULL UNIQUE,
                pin TEXT NOT NULL, 
                balance INTEGER DEFAULT 0)
                ; """
        self.cur.execute(query)
        self.conn.commit()

    def menu(self):
        while True:
            print("1. Create an account\n""2. Log into account\n""0. Exit")
            choice = int(input())
            if choice == 1:
                self.create_account()
            elif choice == 2:
                print("Enter your card number:")
                user_card = input()
                print("Enter your PIN:")
                user_pin = input()
                self.login(user_card, user_pin)
            elif choice == 0:
                print("Bye!")
                exit()

    @staticmethod
    def generate_card():
        random_number = ''.join([str(n) for n in sample(range(9), 9)])
        random_card = int('400000' + ''.join((str(i) for i in random_number)))
        random_pin = (''.join([str(n) for n in sample(range(9), 4)]))
        return random_card, random_pin

    @staticmethod
    def luhn_algo(card):
        card_list_temp = [int(i) for i in str(card)]
        card_list = []
        for x in range(len(card_list_temp)):
            x += 1
            if x % 2 != 0:
                if card_list_temp[x - 1] * 2 > 9:
                    card_list.append(card_list_temp[x - 1] * 2 - 9)
                else:
                    card_list.append(card_list_temp[x - 1] * 2)
            else:
                card_list.append(card_list_temp[x - 1])
        checksum = [i for i in range(0, 9) if (sum(card_list) + i) % 10 == 0]
        card_list_temp.extend(checksum)
        credit_card = int(''.join(str(i) for i in card_list_temp))
        return credit_card

    def check_card(self, card):
        query = """SELECT number FROM card WHERE number = ?"""
        tup = (card,)
        self.cur.execute(query, tup)
        rows = self.cur.fetchone()
        if rows:
            credit_card = (''.join([str(x) for x in rows]))
            return credit_card
        else:
            return False

    def add_card(self, number, pin, balance=0):
        query = "INSERT INTO card (number, pin, balance) VALUES (?, ?, ?);"
        self.cur.execute(query, (number, pin, balance))
        self.conn.commit()

    def read_card(self, card, pin):
        query = """SELECT number, pin FROM card WHERE number = ? AND pin = ?"""
        card_pin_tuple = (card, pin)
        self.cur.execute(query, card_pin_tuple)
        rows = self.cur.fetchone()
        return rows

    def delete_account(self, card, pin):
        query = """DELETE FROM card WHERE number = ? AND pin = ?;"""
        card_pin_tuple = (card, pin)
        self.cur.execute(query, card_pin_tuple)
        self.conn.commit()

    def read_balance(self, card, pin):
        query = """SELECT balance FROM card WHERE number = ? AND pin = ?"""
        card_pin_tuple = (card, pin)
        self.cur.execute(query, card_pin_tuple)
        rows = self.cur.fetchone()
        balance = (''.join([str(x) for x in rows]))
        return balance

    def transfer_money(self, card, pin, card_transfer, money):
        query = """UPDATE card set balance = balance + ? WHERE number = ?"""
        query2 = """UPDATE card set balance = balance - ? WHERE number = ? AND pin = ?"""
        data = (money, card_transfer)
        data2 = (money, card, pin)
        self.cur.execute(query, data)
        self.cur.execute(query2, data2)
        self.conn.commit()

    def create_account(self):
        self.credit_card, self.pin = self.generate_card()
        self.credit_card = self.luhn_algo(self.credit_card)
        while len(str(self.credit_card)) < 16:
            self.credit_card, self.pin = self.generate_card()
            self.credit_card = self.luhn_algo(self.credit_card)
        self.add_card(self.credit_card, self.pin)
        print(f"\nYour card has been created\nYour card number:\n{self.credit_card}")
        print(f"Your card PIN\n{self.pin}\n")

    def login(self, user_card, user_pin):
        cards = self.read_card(user_card, user_pin)
        if cards:
            print("\nYou have successfully logged in!")
            while True:
                print("\n1. Balance\n2. Add income\n"
                      "3. Do transfer\n4. Close account\n5. Log out\n0. Exit")
                choice = int(input())
                if choice == 1:
                    balance = self.read_balance(user_card, user_pin)
                    print(f"\nBalance: {balance}")
                elif choice == 2:
                    income = int(input("\nEnter income:\n"))
                    query = """UPDATE card set balance = balance + ? WHERE number = ? AND pin = ?"""
                    data = (income, user_card, user_pin)
                    print("Income was added!")
                    self.cur.execute(query, data)
                    self.conn.commit()
                elif choice == 3:
                    print("Transfer\nEnter card number:")
                    card_transfer = input()
                    luhn_v = self.luhn_algo(card_transfer[0:-1])
                    if card_transfer == user_card:
                        print("You can't transfer money to the same account!")
                    elif card_transfer[-1] != str(luhn_v)[-1]:
                        print("Probably you made a mistake in the card number. Please try again!")
                    elif not self.check_card(card_transfer):
                        print("Such a card does not exist.")
                    else:
                        print("Enter how much money you want to transfer:")
                        money = int(input())
                        if money > int(self.read_balance(user_card, user_pin)):
                            print("Not enough money!")
                        else:
                            self.transfer_money(user_card, user_pin, card_transfer, money)
                            print("Success!")
                elif choice == 4:
                    self.delete_account(user_card, user_pin)
                    print("\nThe account has been closed!\n")
                    self.menu()
                    break
                elif choice == 5:
                    print("You have successfully logged out!\n")
                    self.menu()
                    break
                elif choice == 0:
                    print("Bye!")
                    exit()
        else:
            print("Wrong card number or PIN!\n")


user = Banking()
user.menu()
