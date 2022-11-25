import firebase_admin
from firebase_admin import credentials, db
import json
import requests
from csv import DictReader
from traceback import format_list

databaseURL = "https://easywareph-2f473-default-rtdb.asia-southeast1.firebasedatabase.app/"


class FireDataBase():
    def __init__(self):
        cred = credentials.Certificate("keyServiceAccount.json")

        firebase_admin.initialize_app(
            cred, {'databaseURL': databaseURL})

    def addUser(self, accountType, username, password, imagePath, fullName, position):
        # Included user mode (Admin 1  or Employee 0)
        try:
            ref = db.reference('/users')
            x = ref.get(False, True)
            items = []
            for i in x.keys():
                items.append(i)
            if username in items:
                return False
            else:
                ref = db.reference(f'/users/{username}')
                content = {
                    "username": username,
                    "accountType": accountType,
                    "password": password,
                    "imagePath": imagePath,
                    "fullName": fullName,
                    "position": position,
                    "cart": ""}
                x = ref.set(content)
                return True
        except:
            ref = db.reference(f'/users/{username}')
            content = {
                "username": username,
                "accountType": accountType,
                "password": password,
                "imagePath": imagePath,
                "fullName": fullName,
                "position": position,
                "cart": ""}
            x = ref.set(content)
            return True

    def getCart(self, username):
        try:
            ref = db.reference(f'/users/{username}/cart')
            cart = ref.get()
            if cart:
                for i in cart:
                    itemDetail = self.readItem(i['itemID'])
                    if itemDetail == False:
                        self.delCart(username, i['itemID'])
                        cart = ref.get()
                    else:
                        i['price'] = itemDetail['price']
                        i['name'] = itemDetail['name']
                        i['image'] = itemDetail['image']
                if cart == None:
                    return False  # If the cart was emptied due to deleted item
                else:
                    return cart
            else:
                return False
        except:
            return False  # Cart empty or user empty

    def delCart(self, username, itemID=0):
        try:
            ref = db.reference('/users')
            x = ref.get(False, True)
            users = []
            for i in x.keys():
                users.append(i)
            if username in users:
                ref = db.reference(f'/users/{username}/')
                data = ref.get()
                cart = data['cart']
                if not cart:
                    return False  # Cart already empty
                else:
                    if itemID == 0:
                        ref = db.reference(f'/users/{username}/cart')
                        ref.set("")
                        return True  # User Cart emptied
                    else:
                        for i in cart:
                            if i['itemID'] == itemID:
                                cart.remove(i)
                        ref = db.reference(f'/users/{username}/cart')
                        ref.set(cart)
                        return True  # Cart removed specific
            else:
                return False  # User nonexistent
        except:
            return False  # DB empty

    def updateCartItemQty(self, username, itemID, quantity):
        try:
            ref = db.reference('/users')
            x = ref.get(False, True)
            users = []
            for i in x.keys():
                users.append(i)
            if username in users:
                cart = self.getCart(username)
                itemList = []
                for i in cart:
                    itemList.append(i['itemID'])
                if itemID in itemList:
                    for i in cart:
                        if i['itemID'] == itemID:
                            if i['quantity'] == quantity:
                                return False  # Duplicated entry
                            else:
                                i['quantity'] = quantity
                    ref = db.reference(f'/users/{username}/cart')
                    ref.set(cart)
                    return True  # Quantity edited
                else:
                    return False  # Item not in cart
            else:
                return False  # User nonexistent
        except:
            return False  # DB empty

    def addToCart(self, username, itemID):
        try:
            ref = db.reference('/users')
            x = ref.get(False, True)
            users = []
            if self.readItem(itemID):
                pass
            else:
                return False
            for i in x.keys():
                users.append(i)
            if username in users:
                ref = db.reference(f'/users/{username}/cart')
                cart = ref.get()
                if not cart:
                    cart = []
                    cart.append({
                        "itemID": itemID,
                        "quantity": 1})
                    ref.set(cart)
                    return True
                else:
                    cart = self.getCart(username)
                    itemList = []
                    for i in cart:
                        itemList.append(i['itemID'])
                    if itemID not in itemList:
                        cart.append({
                            "itemID": itemID,
                            "quantity": 1})
                        ref.set(cart)
                        return True
                    else:
                        for i in cart:
                            if i['itemID'] == itemID:
                                i['quantity'] += 1
                        ref.set(cart)
                        return True
        except:
            return False

    def testing(self):
        ref = db.reference('/items/1910')
        ref.delete()

    def getUser(self, username=''):
        try:
            ref = db.reference('/users')
            x = ref.get(False, True)
            users = []
            for i in x.keys():
                users.append(i)
            if username == '':
                userList = []
                ref = db.reference('/users/')
                x = ref.get(False, False)
                for user in x:
                    userList.append(x[user])
                return userList
            else:
                ref = db.reference(f'/users/{username}')
                result = ref.get()
                if result:
                    return result
                else:
                    return False
        except:
            return False

    def authLogin(self, username, password):
        try:
            ref = db.reference('/users')
            x = ref.get(False, True)
            users = []
            for i in x.keys():
                users.append(i)
            if username in users:
                ref = db.reference(f'/users/{username}')
                correctPassword = ref.get()['password']
                if password == correctPassword:
                    return True, ref.get()['accountType']
                else:
                    return False
            else:
                return False
        except:
            return False

    def updateUser(self, username, mode, newData):  # , mode, content
        # Mode = what will be updated
        # 1 = password, 2 = fullName 3 = accountType
        # It's not allowed to change username.
        try:
            ref = db.reference('/users')
            x = ref.get(False, True)
            users = []
            for i in x.keys():
                users.append(i)
            if username in users:
                userData = db.reference(f'/users/{username}').get()
                if mode == 1:
                    if newData != userData['password']:
                        ref = db.reference(f'/users/{username}/password')
                        ref.set(newData)
                        return True
                    else:
                        return False
                if mode == 2:
                    if newData != userData['fullName']:
                        ref = db.reference(f'/users/{username}/fullName')
                        ref.set(newData)
                        return True
                    else:
                        return False
                if mode == 3:
                    if newData != userData['accountType']:
                        ref = db.reference(f'/users/{username}/accountType')
                        ref.set(newData)
                        return True
                    else:
                        return False
            else:
                return False
        except:
            return False

    def delUser(self, username):
        try:
            ref = db.reference('/users')
            x = ref.get(False, False)
            users = []
            for i in x.keys():
                users.append(i)
            if username in users:
                ref = db.reference(f'/users/{username}')
                ref.delete()
                return True
            else:
                return False
        except:
            return False

    def getNewItemID(self):
        ref = db.reference('/items')
        x = ref.get(False, True)
        items = []
        for i in x.keys():
            items.append(int(i))
        lastNumer = sorted(items)[-1] + 1
        return lastNumer

    def createItem(self, itemID, ITEM):
        if itemID == 0:
            itemID += 1  # ItemID 0 is reserved for getAll
        items = []
        try:
            ref = db.reference('/items')
            x = ref.get(False, True)
            for i in x.keys():
                items.append(int(i))
        except:
            pass
        if itemID in items:
            print(f"Item {itemID} already exists")
            return False
        else:
            ref = db.reference(f'/items/{itemID}')
            ITEM['itemID'] = itemID  # Added itemID val
            ref.set(ITEM)
            return True

    def readItem(self, ID=0):
        if ID == 0:  # Read All items
            try:
                ref = db.reference('/items')
                x = ref.get(False, True)
                items = []
                for i in x.keys():
                    items.append(int(i))
                sampleItems = (sorted(items))
                ref = db.reference('/items/')
                x = ref.get(False, False)
                for item in x.copy():
                    if item is None:
                        x.remove(item)
                return x
            except:
                return False  # Returns False if db is empty/does not exist
        else:  # Read single item
            ref = db.reference(f'/items/{ID}')
            temp = ref.get()
            if temp:
                return temp
            else:
                return False  # Nonexistent

    def updateItem(self, ID, ITEM):
        try:
            ref = db.reference('/items')
            x = ref.get(False, True)
            items = []
            for i in x.keys():
                items.append(int(i))
            if ID in items:
                ref = db.reference(f'/items/{ID}')
                oldItem = ref.get()
                if oldItem['name'] == ITEM['name'] and oldItem['price'] == ITEM['price']:
                    return False
                ref.set(ITEM)
                return True
            else:
                return False  # Item ID does not exist
        except:
            return False  # Returns False if db is empty/does not exist

    def deleteItem(self, ID):
        try:
            ref = db.reference('/items')
            x = ref.get(False, True)
            items = []
            for i in x.keys():
                items.append(int(i))
            if ID in items:
                ref = db.reference(f'/items/{ID}')
                ref.delete()
                return True
            else:
                return False
        except:
            return False


if __name__ == '__main__':
    app = FireDataBase()
