import sqlite3
from datetime import date
from csv import DictReader


def populateDatabase():
    with open('RES/item_details.csv', 'r') as dataFile:
        i = 1
        temp = DictReader(dataFile)
        sample = list(temp)
        newDict = {}
        for data in sample:
            for entry in data:
                newDict[entry.replace("'", "")] = data[entry].replace("'", "")
            app.insert_item(i, newDict, 1, "Erickson")
            i += 1


class SudoApp():
    conn = sqlite3.connect('EasyWare_Local')
    sqlitedb = conn.cursor()

    def __init__(self):
        self.sqlitedb.execute('''
                CREATE TABLE IF NOT EXISTS items
                ([itemID] INTEGER PRIMARY KEY, [name] TEXT, [price] REAL, [stocks] INTEGER, [image] TEXT, [info] TEXT, [brand] TEXT)
                ''')
        self.conn.commit()
        # check update to the firebase
        # if new update is available, update the content of SQLITE db
        # else do nothing

        # What if we create a child based on "datetoday" of timeanddate module

    def GetAllItems(self):
        # Get all of the items sorted by ID
        self.sqlitedb.execute("""SELECT * FROM items""")
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
            print('There is no item number %i' % item_id)
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
            try:
                self.sqlitedb.execute('''INSERT INTO items VALUES(?,?,?,?,?,?,?)''',
                                      (item_id, name, price, stocks, image, info, brand))
                self.conn.commit()
                self.log(username, f"Added item {item_id}: {name}")
                return True
            except sqlite3.IntegrityError as e:
                print(f'Item {item_id} already exist.', e.args[0])
                return False
        else:
            return False

    def log(self, user, message):
        f = open(f"{user}_log.txt", "a")
        time = date.today()
        f.write(f"{message}\n {time}\n")
        f.close()

    def update():
        # updates the firebase
        pass


app = SudoApp()
sampleItem = {"name": "Allen Key", "price": 320.5, "stocks": 42,
              "image": "RES/RES/allenKey.jpg", "info": "lorem ips", "brand": "BondHus"}
editedItem = {"name": "qweqweqwe", "price": 320.5, "stocks": 42,
              "image": "RES/RES/allenKey.jpg", "info": "lorem ips", "brand": "BondHus"}
# app.delete_item(5,True,"Erickson")
#app.insert_item(1,sampleItem,True, "Erickson")
# print(app.get_item(1))
app.delete_item(1, True, "Erickson")
# app.update_item(1,editedItem,1,"Erickson")
# print(app.get_item(1))
# app.delete_item(2,1,"Erickson")
populateDatabase()
print(app.GetAllItems())
#
