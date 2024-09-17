'''

Project one Fridge inventory system

'''

import sqlite3
import datetime
'''
class Item:
    def __init__(self):
        self.__quantity = 0
        self.__name = ""
        self.__expiration = ""

    def add_item(self, quantity, name, expiration):
        self.__quantity = quantity
        self.__name = name
        self.__expiration = expiration

    def get_item(self):
        return self.__name
'''
class Database:
    def __init__(self):
        self.items = sqlite3.connect("items.db")
        self.cur = self.items.cursor()

        if not self.table_exists("fridge_contents"):
            self.cur.execute('''CREATE TABLE IF NOT EXISTS fridge_contents
                            (name TEXT PRIMARY KEY,
                            quantity INTEGER,
                            expiration TEXT)''')

        if not self.table_exists("volumes"):
            self.cur.execute('''CREATE TABLE IF NOT EXISTS volumes
                            (name TEXT PRIMARY KEY,
                            volume INTEGER)''')

        self.items.commit()

    def table_exists(self, table_name):
        self.cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
        result = self.cur.fetchone()
        return result is not None

    def insert_into_fridge_contents(self, name, quantity, expiration):
        self.cur.execute("INSERT OR REPLACE INTO fridge_contents (name, quantity, expiration) VALUES (?, ?, ?)", (name, quantity, expiration))
        self.items.commit()

    def update_fridge_contents(self, name, quantity, expiration):
        self.cur.execute("UPDATE fridge_contents SET quantity = ? WHERE name = ? AND expiration = ?",(quantity, name, expiration))
        self.items.commit()

    def delete_fridge_contents(self, name, expiration):
        self.cur.execute("DELETE FROM fridge_contents WHERE name = ? AND expiration = ?",(name, expiration))
        self.items.commit()

    def show_fridge_contents(self):
        self.cur.execute("SELECT * FROM fridge_contents")

        self.rows = self.cur.fetchall()

        print(f"\n{'NAME':<10}{'QUANTITY':<10}{'EXPIRATION':<10}")
        print("-" * 30)

        for row in self.rows:
            print(f"{row[0]:<10}{row[1]:<10}{row[2]:<10}")

    def insert_into_volumes(self, name, volume):
        self.cur.execute("INSERT OR REPLACE INTO volumes (name, volume) VALUES (?, ?)", (name, volume))
        self.items.commit()

    def update_volumes(self, name, volume):
        self.cur.execute("UPDATE fridge_contents SET volume = ? WHERE name = ? AND expiration = ?",(volume, name))
        self.items.commit()

    def delete_volumes(self, name, volume):
        self.cur.execute("DELETE FROM volumes WHERE name = ? AND volume = ?",(name, volume))
        self.items.commit()

    def empty_fridge(self):
        self.cur.execute("DELETE from fridge_contents")
        self.items.commit()

    def remove_expired(self):
        self.cur.execute("DELETE from fridge_contents WHERE expiration < DATE('now')")
        self.items.commit()

    def show_volumes(self):
        self.cur.execute("SELECT * FROM volumes")

        self.rows = self.cur.fetchall()

        print(f"{'NAME':<10}{'VOLUME':<10}")
        print("-" * 20)

        for row in self.rows:
            print(f"{row[0]:<10}{row[1]:<10}")

def main():
    db = Database()
    choice = ""
    name = ""
    qty = 0
    date = ""

    while choice != '0': # prompt for user input in menu
        print("\n1 - Add something to the fridge")
        print("2 - Remove something from the fridge")
        print("3 - View fridge contents")
        print("4 - Remove expired items")
        print("5 - Empty fridge")
        print("0 - Exit")
        choice = input("What would you like to do? ")

        if choice == '0': # exit case
            print("Exiting...")
        elif choice == '1': # add to fridge using UI
            name = input("What are you adding? ")
            qty = input("How many? ")
            date = input("When does it expire (YYYY/MM/DD)? ")
            year,month,day = map(int,date.split('/'))
            exp_date = datetime.date(year, month, day)
            db.insert_into_fridge_contents(name, qty, exp_date)
            db.show_fridge_contents()
        elif choice == '2': # remove from fridge using UI
            name = input("What are you removing? ")
            date = input("When does it expire (YYYY/MM/DD)? ")
            year, month, day = map(int, date.split('/'))
            exp_date = datetime.date(year, month, day)
            db.delete_fridge_contents(name, exp_date)
            db.show_fridge_contents()
        elif choice == '3': # show contents of fridge
            db.show_fridge_contents()
        elif choice == '4': # NEED TO IMPLEMENT compare db entries expiration against today
            print("Removing expired items...")
            db.remove_expired()
            db.show_fridge_contents()
        elif choice == '5':
            db.empty_fridge()
            db.show_fridge_contents()
        else:
            print("\nUnknown input, try again!")
            continue

main()
