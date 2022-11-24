import sqlite3
from datetime import date
from csv import DictReader
from ast import literal_eval


def populateDatabase():
    with open('RES/CSVs/item_details.csv', 'r') as dataFile:
        i = 1
        temp = DictReader(dataFile)
        sample = list(temp)
        newDict = {}
        for data in sample:
            for entry in data:
                newDict[entry.replace("'", "")] = data[entry].replace("'", "")
            SudoApp().insert_item(i, newDict, 1, "Erickson")
            i += 1


class SudoApp():
    conn = sqlite3.connect('EasyWare_Local')
    sqlitedb = conn.cursor()

    def __init__(self):
        self.sqlitedb.execute('''
                CREATE TABLE IF NOT EXISTS items
                ([itemID] INTEGER, [name] TEXT, [price] INTEGER, [image] TEXT, [info] TEXT, [type] TEXT, [stocks] INTEGER, [brand] TEXT, [color] TEXT)
                ''')
        self.conn.commit()
        # INITIALIZATION FOR USER TABLE
        self.sqlitedb.execute('''
                CREATE TABLE IF NOT EXISTS users
                ([username] TEXT PRIMARY KEY, [password] TEXT, [accountType] INTEGER, [fullName] TEXT, [cart] TEXT NULL)
                ''')

        self.conn.commit()

        # check update to the firebase
        # if new update is available, update the content of SQLITE db
        # else do nothing

        # What if we create a child based on "datetoday" of timeanddate module
    def CreateUser(self, username, password, accountType, fullName):
        try:
            self.sqlitedb.execute('''INSERT INTO users VALUES(?,?,?,?,"")''',
                                  (username, password, accountType, fullName))
            self.conn.commit()
            self.logUser(
                username, f'User({"Admin" if accountType==1 else "Employee"}): {username} with a password of {password} added')

            return True
        except sqlite3.IntegrityError as e:
            print(f'User: {username} already exist.', e.args[0])
            return False

    def authLogin(self, username, password):
        self.sqlitedb.execute(
            "SELECT count(*) FROM users WHERE username = ? AND password = ? ", (username, password))
        db_result = self.sqlitedb.fetchone()[0]
        if db_result != 0:
            return True
        else:
            return False

    def addToCart(self, username, itemID, quantity):
        self.sqlitedb.execute(
            """SELECT cart FROM users WHERE username = ?""", ([username]))
        cartItems = self.sqlitedb.fetchone()
        newCart = ""
        if cartItems[0] == "":
            newCart = (str("{'itemID':") + str(itemID) + "," +
                       "'quantity':" + str(quantity) + "}" + ",")
        else:
            oldCart = cartItems[0]
            newCart = oldCart + (str("{'itemID':") + str(itemID) + "," +
                                 "'quantity':" + str(quantity) + "}" + ",")

        self.sqlitedb.execute('''UPDATE users SET cart = ? WHERE username = ? ''',
                              (str(newCart), username))
        self.conn.commit()

    def editCart(self, username, cart):
        self.sqlitedb.execute('''UPDATE users SET cart = ? WHERE username = ? ''',
                              (cart, username))
        self.conn.commit()
        return True

    def clearCart(self, username):
        self.sqlitedb.execute('''UPDATE users SET cart = ? WHERE username = ? ''',
                              ("", username))
        self.conn.commit()

    def getCart(self, username):
        self.sqlitedb.execute(
            """SELECT cart FROM users WHERE username = ?""", ([username]))
        cartItems = literal_eval(self.sqlitedb.fetchone()[0])
        CartData = []
        i = 1
        try:
            for x in cartItems:
                y = x.split("|")
                for items in y:
                    items = items.split(",")
                    CartData.append(
                        {"Entry": i, "ItemID": items[0], "Quantity": items[1]}
                    )
                    i += 1
            print(CartData)
            return CartData
        except:
            print(f"There are no items in {username}'s cart.")
            return False

    def GetAllItems(self, sortBy="id", desc=True, limit=0):
        # Get all of the items sorted by input
        if limit > 0:
            if desc:
                self.sqlitedb.execute(
                    f"""SELECT * FROM items ORDER BY {sortBy.replace("'", "")} DESC LIMIT {limit}""")
            else:
                self.sqlitedb.execute(
                    f"""SELECT * FROM items ORDER BY {sortBy.replace("'", "")} ASC LIMIT {limit}""")
        else:
            if desc:
                self.sqlitedb.execute(
                    f"""SELECT * FROM items ORDER BY {sortBy.replace("'", "")} DESC""")
            else:
                self.sqlitedb.execute(
                    f"""SELECT * FROM items ORDER BY {sortBy.replace("'", "")} ASC""")

        items = self.sqlitedb.fetchall()
        x = []
        for item in items:
            x.append({'itemID': item[0], 'name': item[1], 'price': item[2],
                     'image': item[3], 'info': item[3], 'stocks': item[4], 'brand': item[5]})
        return x

    def get_item(self, item_id):
        # Get Item by item ID query
        self.sqlitedb.execute(
            "SELECT count(*) FROM items WHERE itemID = ?", (item_id,))
        db_result = self.sqlitedb.fetchone()[0]
        if db_result == 0:
            print('Item Does not Exist')
            return False
        else:
            self.sqlitedb.execute(
                "SELECT * FROM items WHERE itemID=?;", (str(item_id)))
            sample = self.sqlitedb.fetchone()
            item = {
                'name': sample[0],
                'price': sample[1],
                'image': sample[2],
                'info': sample[3],
                'stocks': sample[4],
                'brand': sample[5]
            }
            return item

    def update_item(self, item_id, item_json, user, username):
        # Only admin user can edit, logs edited item
        name = item_json['name']
        price = item_json['price']
        stocks = item_json['stocks']
        image = item_json['image']
        info = item_json['info']
        brand = item_json['brand']
        if user:
            self.sqlitedb.execute(
                "SELECT count(*) FROM items WHERE itemID = ?", (item_id,))
            db_result = self.sqlitedb.fetchone()[0]
            if db_result == 0:
                print('There is no item number %i' % item_id)
                return False
            else:
                self.sqlitedb.execute("UPDATE items SET name = ?, price = ?, image = ?, info = ?, stocks = ?, brand = ? WHERE itemID = ?", (
                    name, price, stocks, image, info, brand, item_id))
                self.log(
                    username, f"Updated item number {item_id} to: {item_json}")
                return True

    def delete_item(self, item_id, user, username):
        # Only admin user can delete items, logged.
        if user:
            self.sqlitedb.execute(
                "DELETE FROM items WHERE itemID=?", (item_id,))
            self.conn.commit()
            self.log(username, f"Deleted item {item_id}")
            return True
        # returns boolean
        else:
            return False

    def insert_item(self, item_id, item_json, user, username):
        # Only admin user can insert item, logged.
        if user:
            name = item_json['name']
            price = item_json['price']
            stocks = item_json['stocks']
            image = item_json['image']
            info = item_json['info']
            brand = item_json['brand']
            color = item_json['color']
            itemType = item_json['type']
            try:
                self.sqlitedb.execute('''INSERT INTO items VALUES(?,?,?,?,?,?,?,?,?)''',
                                      (item_id, name, price, image, info, itemType, stocks, brand, color))
                self.conn.commit()
                self.log(username, f"Added item {item_id}: {name}")
                return True
            except sqlite3.IntegrityError as e:
                print(f'Item {item_id} already exist.', e.args[0])
                return False
        else:
            return False

    def log(self, user, message):
        #f = open(f"{user}_log.txt", "a")
        #time = date.today()
        #f.write(f"{message}\n {time}\n")
        # f.close()
        pass

    def logUser(self, user, message):
        #f = open(f"Users_log.txt", "a")
        #time = date.today()
        #f.write(f"{message}\n {time}\n")
        # f.close()
        pass

    def update():
        # updates the firebase
        pass


app = SudoApp()
sampleItem = {"name": "Allen Key", "price": 320.5, "stocks": 42,
              "image": "RES/RES/allenKey.jpg", "info": "lorem ips", "brand": "BondHus"}
editedItem = {"name": "qweqweqwe", "price": 320.5, "stocks": 42,
              "image": "RES/RES/allenKey.jpg", "info": "lorem ips", "brand": "BondHus"}
# app.delete_item(5,True,"Erickson")
# app.insert_item(1,sampleItem,True, "Erickson")
# print(app.get_item(1))
# app.delete_item(1, True, "Erickson")
# app.update_item(1,editedItem,1,"Erickson")
# print(app.get_item(1))
# app.delete_item(2,1,"Erickson")
# print(app.GetAllItems())
# populateDatabase()
# print(app.CreateUser("Erickson", "123123", 1, "Erickson Dela Soledad"))
# user Erickson orders 5 tiles and 2 tile grout
# print(app.AddToCart("Erickson", 40, 5))
# print(app.AddToCart("Erickson", 39, 2))
# print(app.CreateUser("User2", "123123", 0, "Dummy User 2"))
# print(app.CreateUser("User3", "12221", 0, "user 4"))
# print(app.CreateUser("Lorem", "3333", 0, "ABC User"))
# print(app.CreateUser("Dolor", "333123", 1, "BLABLABOOM"))
# app.editCart("Erickson", "40,5|39,2")
# app.getCart("Erickson")
# app.clearCart("Erickson")
# app.getCart("Erickson")
# populateDatabase()
# data = app.GetAllItems("price", 1, 100) !! ADDING THE THIRD PARAMETER SETS A LIMIT FOR ITEMS !!
data = app.GetAllItems("price", 1)  # 0 = ascending
#                                     1 = descending (BOOLEAN)
x = 0
print("--------------\n")
for index in data:
    if x != 200:
        print(index['name'], index['price'])
    else:
        break

    # for key, value in index.items():
    #     print(f'{key}: {value}')
print("--------------\n")
