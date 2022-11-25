from sudoAPP import FireDataBase
from csv import DictReader


def populateDatabase(MAX=1001):
    with open('RES/item_details.csv', 'r') as dataFile:
        i = 1
        temp = DictReader(dataFile)
        sample = list(temp)
        newDict = {}
        for data in sample:
            for entry in data:
                newDict[entry.replace("'", "")] = data[entry].replace("'", "")
                newDict['itemID'] = i
            print(app.createItem(i, newDict))
            i += 1
            if i == MAX+1:
                break


sampleItem = {"name": "Allen Key", "price": 320.5, "stocks": 42,
              "image": "RES/RES/allenKey.jpg", "info": "lorem ips", "brand": "BondHus"}
editedItem = {"name": "qweqweqwe", "price": 320.5, "stocks": 42,
              "image": "RES/RES/allenKey.jpg", "info": "lorem ips", "brand": "BondHus"}
sampleUser1 = 1, "Erickson", "123", "Erickson Dela Soledad"
sampleUser2 = 0, "ABSON", "123", "Erickson Dela Soledad"
sampleUser3 = 1, "RONELG", "123", "Erickson Dela Soledad"
sampleUserUpdate1 = None
if __name__ == '__main__':
    app = FireDataBase()
    # populateDatabase()
    # app.readItem()
    # app.createItem(1, sampleItem)
    # app.updateItem(1000, editedItem)
    # print(app.readItem())
    # populateDatabase(2)
    # Example on how to use get next available num
    # print(app.createItem(app.getNewItemID(), sampleItem))
    # print(app.addUser(*sampleUser1))
    # print(app.addUser(*sampleUser2))
    # print(app.addUser(*sampleUser3))
    # print(app.getUser("Erickson"))  # Get one user
    # print(app.getUser("WrongInput"))  # Get wrong user
    # print(app.getUser())  # Get all User in listed form
    # print(app.authLogin("Erickson", "123"))  # Auth right
    # print(app.authLogin("Erickson", "333"))  # Auth wrong
    # print(app.authLogin("Nobody", "Nothing"))  # Auth nonexistent user

    # print(app.addUser(*sampleUser1))
    # print(app.addUser(*sampleUser2))
    # print(app.addUser(*sampleUser3))
    # print(app.updateUser("Nobody", 1, "1222")) # Edit nonexistent user
    # print(app.updateUser("Erickson", 1, "123"))  # Enter the same password
    # print(app.updateUser("Erickson", 1, "Ulan123"))  # Enter a new password
    # Enter the same fullname
    # print(app.updateUser("Erickson", 2, "Erickson Dela Soledad"))
    # print(app.updateUser("Erickson", 2, "Ericky Montogomery"))# Enter a new fullname
    # print(app.updateUser("Erickson", 3, 1))  # Enter same account Type
    # print(app.updateUser("Erickson", 3, 0))  # Enter different account Type
    # print(app.addUser(*sampleUser1))
    # print(app.addUser(*sampleUser2))
    # print(app.addUser(*sampleUser3))
    # print(app.delUser("Erickson"))  # Delete an existing user
    # print(app.delUser("Nobodyl"))  # Delete a nonexistent user
    # app.addToCart("ABC", 1)
    # print(app.getUser("AWEAS"))
    # print(app.addToCart("Erickson", 1))
    # print(app.addToCart("Erickson", 2))
    # print(app.addToCart("Erickson", 194))
    # print(app.addToCart("Erickson", 205))
    # print(app.getCart("Erickson"))
    # print(app.addToCart("RONELG", 1))

    # Del specific item on cart demo
    # print(app.addUser(*sampleUser1))
    # print(app.addToCart("Erickson", 1))
    # print(app.addToCart("Erickson", 2))
    # print(app.addToCart("Erickson", 194))
    # print(app.addToCart("Erickson", 205))
    # print(app.delCart("Erickson", 1))

    # Edit quanity on cart
    # print(app.addUser(*sampleUser1))
    # print(app.addUser(*sampleUser3))

    # print(app.addToCart("Erickson", 1))
    # print(app.addToCart("Erickson", 2))
    # print(app.addToCart("Erickson", 194))
    # print(app.addToCart("Erickson", 205))
    # print(app.updateCartItemQty("Erickson", 205, 102))  # Item not in cart
    # print(app.updateCartItemQty("Erickson", 2, 502))  # Item not in cart
    # print(app.updateCartItemQty("Erickson", 2, 502))  # Same data to input
    # print(app.updateCartItemQty("RONELG", 1, 202)) # Cart empty
    # print(app.getCart("Erickson")[0])

    # print(app.addUser(1, "Cruzandlex", "12345", "Zandlex Cruz", "staff"))
    user = "test"
    # print(app.addToCart(user, 105))
    # print(app.getCart("Cruzandlex"))
    # print(app.delCart("Erickson", 1))
    # print(app.getCart("Erickson"))

    # print(app.addUser(1, user, "12345", "Zandlex Cruz", "staff"))
    # print(app.addToCart(user, 2))
    # print(app.getCart(user))
    # print(app.readItem()[0])
    # app.testing()
    item = app.readItem(50)
    print(item['name'])
    app.updateItem(49, item)
