from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.core.text import LabelBase
from kivy.properties import StringProperty
from kivymd.uix.card import MDCard
from sudoAPP import FireDataBase
import threading

Window.size = (270, 550)
LabelBase.register(name = "Nunito", fn_regular= "RES/fonts/BebasNeue-Regular.otf")
LabelBase.register(name = "TypeWriter", fn_regular= "RES/fonts/atwriter.ttf")

class RecycleCard(MDCard):      #Custom card for the recycle view
    image = StringProperty()
    name = StringProperty()
    price = StringProperty()
    id = StringProperty()
class RecycleCardCart(MDCard):      #Custom card for the recycle view
    image = StringProperty()
    name = StringProperty()
    price = StringProperty()
    total = StringProperty()
    quantity = StringProperty()
    id = StringProperty()
class UsersRecycleCard(MDCard):      #Custom card for the recycle view
    image = StringProperty()
    name = StringProperty()
    position = StringProperty()
    userName = StringProperty()
    updatedUserName = StringProperty()
    userType = StringProperty()
class CheckoutRecycleCard(MDCard):      #Custom card for the recycle view
    name = StringProperty()
    price = StringProperty()
    quantity = StringProperty()
    id = StringProperty()
class EasyWare(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs) 
        self.screen = Builder.load_file('KV/main.kv')
        self.backEnd = FireDataBase()
        self.cart = []
        self.userType = '0'
        self.username = ''
        self.items = self.backEnd.readItem()
        self.reloadAll()
            
    def auth(self,username,password):
        if self.backEnd.authLogin(username,password)[0]:
            self.username = username
            self.userType = self.backEnd.authLogin(username,password)[1]
            self.reloadCart()
            if self.userType == '0':
                holder = self.backEnd.getUser(username)
                self.screen.ids.user.ids.fullName.text = holder['fullName']
                self.screen.ids.user.ids.position.text = holder['position']
                self.screen.ids.user.ids.profileImage.source = holder['imagePath']
                self.screen.current = 'user'
            else:
                holder = self.backEnd.getUser(username)
                self.screen.ids.userAdmin.ids.fullName.text = holder['fullName']
                self.screen.ids.userAdmin.ids.position.text = holder['position']
                self.screen.ids.userAdmin.ids.profileImage.source = holder['imagePath']
                self.screen.current = 'userAdmin'
        else:
            print("Incorrect User or Pass")
            
    def search(self,text):      #Search function for recycle view  
        holder = [{  'image': y['image'],'name': y['name'],'price': str(y['price']), 'id': str(y['itemID'])} for y in self.items if text.lower() in y['name'].lower()]
        self.screen.ids.search.ids.searchrecycleview.data = holder
        self.screen.ids.searchAdmin.ids.searchrecycleview.data = holder
    
    def reloadAll(self):           #Reloads item from database
        holder = [{ 'image': x['image'],'name': x['name'],'price': str(x['price']), 'id': str(x['itemID'])} for x in self.items]
        self.screen.ids.home.ids.homerecycleview.data = holder
        self.screen.ids.search.ids.searchrecycleview.data = holder 
        self.screen.ids.homeAdmin.ids.homerecycleview.data = holder 
        self.screen.ids.searchAdmin.ids.searchrecycleview.data = holder 
        self.screen.ids.usersAdmin.ids.usersrecycleview.data = [{ 'image': x['imagePath'],
                                                                 'name': x['fullName'],
                                                                 'position': str(x['position']), 
                                                                 'userName': str(x['username']),
                                                                 'userType': str(x['accountType'])} for x in self.backEnd.getUser()]
        
    def reloadCart(self):           #Reloads the cart items
        self.cart = self.backEnd.getCart(self.username)
        if self.cart != False:
            self.screen.ids.cart.ids.cartrecycleview.data = [{  'image': z['image'],
                                                                'name': z['name'],
                                                                'total': str(round(float(z['price'])*int(z['quantity']),2)), 
                                                                'quantity': str(z['quantity']),
                                                                'id': str(z['itemID'])
                                                                } for z in self.cart]
            
            self.screen.ids.checkout.ids.checkoutrecycleview.data = [{  'name': a['name'],
                                                                        'price': str(round(float(a['price'])*int(a['quantity']),2)), 
                                                                        'quantity': str(a['quantity']),
                                                                        'id': str(a['itemID'])
                                                                        } for a in self.cart]
        else:
            self.screen.ids.cart.ids.cartrecycleview.data = []
            self.screen.ids.checkout.ids.checkoutrecycleview.data = []
    
    def temp(self, message):    #Temporary printing function
        print(message)
    
    def count(self,action,item):
        try:
            if action == 'add':
                item.quantity = str(int(item.quantity) + 1)
                item.total = str(round(float(self.items[int(item.id)]['price']) * float(item.quantity),2))
            else:
                item.quantity = str(int(item.quantity) - 1)
                item.total = str(round(float(self.items[int(item.id)]['price']) * float(item.quantity),2))
                if int(item.quantity) == 0:
                    self.backEnd.delCart(self.username,item.id)
            self.backEnd.updateCartItemQty(self.username,item.id,item.quantity)
        except:
            pass
        self.reloadCart()
    
    def checkOut(self):
        total = 0
        try:
            for x in self.cart:
                total += float(x['price'])*int(x['quantity'])
                self.screen.ids.checkout.ids.subtotal.text = str(round(total,2))
        except:
            self.screen.ids.checkout.ids.subtotal.text = '0'
            print('empty cart')
        self.screen.current = 'checkout'
    
    def gotoItem(self,itemID):
        try:
            item = self.backEnd.readItem(itemID)
            if self.userType == '0':
                self.screen.ids.item.ids.itemImage.source = item['image']
                self.screen.ids.item.ids.itemID.text = str(item['itemID'])
                self.screen.ids.item.ids.itemName.text = item['name']
                self.screen.ids.item.ids.itemPrice.text  = f"P {item['price']}"
                self.screen.ids.item.ids.itemInfo.text  = f"Item:        {item['name']}\nStocks:        {item['stocks']}\nType:         {item['type']}\nBrand:        {item['brand']}\nColor:         {item['color']}\nItem Details:\n          {item['info']}"
                self.screen.current = 'item'
            else:
                self.screen.ids.itemEdit.ids.itemID.text = str(item['itemID'])
                self.screen.ids.itemEdit.ids.itemImage.source = item['image']
                self.screen.ids.itemEdit.ids.itemName.text = item['name']
                self.screen.ids.itemEdit.ids.itemPrice.text  = str(item['price'])
                self.screen.ids.itemEdit.ids.itemStocks.text  = str(item['stocks'])
                self.screen.ids.itemEdit.ids.itemType.text  = item['type']
                self.screen.ids.itemEdit.ids.itemBrand.text  = item['brand']
                self.screen.ids.itemEdit.ids.itemColor.text  = item['color']
                self.screen.ids.itemEdit.ids.itemInfo.text = item['info']
                self.screen.current = 'itemEdit'
        except:
            self.items = self.backEnd.readItem()
            self.reloadCart()
            self.reloadAll()
            
    def addToCart(self,itemID):
        try:
            self.backEnd.addToCart(self.username,itemID)
            self.reloadCart()
        except:
            self.items = self.backEnd.readItem()
            self.reloadAll()
            self.reloadCart()
            
    def editItem(self,item):
        try:
            editedItem = {"itemID": int(item['itemID']),
                        "name": item['name'], 
                        "price": float(item['price']), 
                        "stocks": int(item['stocks']),
                        "image": item['image'], 
                        "info": item['info'], 
                        "brand": item['brand'],
                        "color" : item['color'],
                        "type" : item['type']}
            self.backEnd.updateItem(int(item['itemID']), editedItem)
        except:
            pass
        self.items = self.backEnd.readItem()
        self.reloadAll()
    
    def gotoUser(self,userName):
        try:
            user = self.backEnd.getUser(userName)
            self.screen.ids.userEdit.ids.fullNameInput.text = user['fullName']
            self.screen.ids.userEdit.ids.userNameInput.text = user['username']
            self.screen.ids.userEdit.ids.userName.text = user['username']
            self.screen.ids.userEdit.ids.passwordInput.text = user['password']
            self.screen.ids.userEdit.ids.positionInput.text = user['position']
            self.screen.ids.userEdit.ids.profileImage.source = user['imagePath']
            self.screen.ids.userEdit.ids.userType.active = bool(int(user['accountType']))
            self.screen.current = 'userEdit'
        except:
            self.reloadAll()
           
    def editUser(self,user):
        try:
            self.backEnd.updateUser(user['userName'],
                                    user['updatedUserName'],
                                    str(int(user['accType'])),
                                    user['fName'],
                                    user['position'],
                                    user['password'])
        except:
            pass
        self.reloadAll()
    
    def deleteUser(self,userName):
        try:
            self.backEnd.delUser(userName)
        except:
            pass
        self.reloadAll()
    
    def addUser(self,user):
        try:
            self.backEnd.addUser(str(int(user['accType'])),user['userNameInput'],user['password'],'RES/Users/userProfile.png',user['fName'],user['position'])
        except:
            pass
        self.reloadAll()
    
    def deleteItem(self,itemID):
        try:
            self.backEnd.deleteItem((int(itemID)))
        except:
            pass
        self.items = self.backEnd.readItem()
        self.reloadAll()
    
    def deleteAllCart(self):
        try:
            self.backEnd.delCart(self.username)
        except:
            pass
        self.reloadCart()
         
    def build(self):
        return self.screen  

if __name__=="__main__":
    EasyWare().run()