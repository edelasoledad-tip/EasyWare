from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.core.text import LabelBase
from kivy.properties import StringProperty
from kivymd.uix.card import MDCard
from EasyWare_SQLiteSudoApp import SudoApp
from sudoAPP import FireDataBase

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
    quantity = StringProperty()
    id = StringProperty()
class UsersRecycleCard(MDCard):      #Custom card for the recycle view
    image = StringProperty()
    name = StringProperty()
    position = StringProperty()
    price = StringProperty() #temporary
    id = StringProperty()
class CheckoutRecycleCard(MDCard):      #Custom card for the recycle view
    name = StringProperty()
    price = StringProperty()
    quantity = StringProperty()
    id = StringProperty()

class EasyWare(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs) 
        self.sudoApp = SudoApp()
        self.screen = Builder.load_file('KV/main.kv')
        self.backEnd = FireDataBase()
        self.items = self.sudoApp.GetAllItems('itemID')
        self.user = ''
        self.cart = []
        self.userType = 'admin'
        self.reloadAll()
    
    def auth(self,username,password):
        if self.sudoApp.authLogin(username,password):
            self.user = username
            self.cart = self.sudoApp.getCart(self.user)
            self.reloadCart()
            if self.userType == 'user':
                self.screen.current = 'user'
            else:
                self.screen.current = 'userAdmin'
        else:
            self.screen.current = 'user'
            
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
        self.screen.ids.usersAdmin.ids.usersrecycleview.data = holder  
        
    def reloadCart(self):           #Reloads the cart items
        if self.cart != None:
            self.screen.ids.cart.ids.cartrecycleview.data = [{  'image': z['image'],
                                                                'name': z['name'],
                                                                'price': str(z['price']), 
                                                                'quantity': str(z['quantity']),
                                                                'id': str(z['itemID'])
                                                                } for z in self.cart]
            
            self.screen.ids.checkout.ids.checkoutrecycleview.data = [{  'name': a['name'],
                                                                        'price': str(a['price']), 
                                                                        'quantity': str(a['quantity']),
                                                                        'id': str(a['itemID'])
                                                                        } for a in self.cart]
        else:
            pass
    
    def temp(self, message):    #Temporary printing function
        print(message)
    
    def count(self,action,item):
        if action == 'add':
            item.quantity = str(int(item.quantity) + 1)
            item.price = str(round(float(self.sudoApp.get_item(int(item.id))['price']) * float(item.quantity),2))
            
        else:
            item.quantity = str(int(item.quantity) - 1)
            item.price = str(round(float(self.sudoApp.get_item(int(item.id))['price']) * float(item.quantity),2))
            if int(item.quantity) < 0:
                self.cart = [{  'image': z['image'],
                                'name': z['name'],
                                'price': z['price'], 
                                'quantity': z['quantity'],
                                'itemID': z['itemID']
                                } for z in self.cart if item.id != z['itemID']]
                self.reloadCart()
    
    def checkOut(self):
        total = 0
        for x in self.cart:
            total += float(x['price'])
        
        self.screen.ids.checkout.ids.subtotal.text = str(round(total,2))
        self.screen.current = 'checkout'
    
    def gotoItem(self,itemID):
        #item = self.sudoApp.get_item(itemID)
        item = self.backEnd.readItem(itemID)
        if self.userType == 'user':
            self.screen.ids.item.ids.itemImage.source = item['image']
            self.screen.ids.item.ids.itemName.text = item['name']
            self.screen.ids.item.ids.itemPrice.text  = f"P {item['price']}"
            self.screen.ids.item.ids.itemInfo.text  = f"Item:        {item['name']}\nStocks:        {item['stocks']}\nType:         {item['type']}\nBrand:        {item['brand']}\nColor:         {item['color']}\nItem Details:\n          {item['info']}"
            self.screen.current = 'item'
        else:
            self.screen.current = 'itemEdit'
           
    def build(self):
        return self.screen  

if __name__=="__main__":
    EasyWare().run()