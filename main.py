from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.core.text import LabelBase
from kivy.uix.floatlayout import FloatLayout
from kivymd.uix.card import MDCard
from kivy.uix.recycleview import RecycleView
from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty, ListProperty
from csv import DictReader
import EasyWare_SQLiteSudoApp as local
# open file in read mode

Window.size = (270, 550)
LabelBase.register(name = "Nunito", fn_regular= "RES/BebasNeue-Regular.otf")

class ScrollCard(MDCard):
    name = StringProperty()
    price = StringProperty()
    image = StringProperty()
    id = 0
class ScrollCard2(MDCard):
    name = StringProperty()
    price = StringProperty()
    image = StringProperty()
    id = 0
class ItemScreen(Screen):
    name = StringProperty()
    price = StringProperty()
    image = StringProperty()
    info = StringProperty()
    id = StringProperty()
class ScrollCardCart(MDCard):
    name = StringProperty()
    price = StringProperty()
    image = StringProperty()
    id = 0
class EasyWareApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen = Builder.load_file('KV/main.kv')
        self.database = local.SudoApp()
        self.home = self.database.GetAllItems() #sqlite items
        self.search = self.database.GetAllItems() #sqlite items
        self.inventory = self.database.GetAllItems()
        Window.bind(on_keyboard=self.Android_back_click)
        
        with open("RES/cart.csv", 'r') as d: #local file that holds the cart items
            self.cart = list(DictReader(d))

        for x in self.home: #loading item widgets on the scrollview for home
            self.card = ScrollCard()
            self.card.ids.homename.text = x['name']
            self.card.ids.homeprice.text = str(x['price'])
            self.card.ids.homeimage.source = x['image']
            self.card.id = x['itemID']
            self.screen.ids.home.ids.homescrollgrid.add_widget(self.card)
        
        for y in self.cart: #loading item widgets on the scrollview for cart
            self.cartcard = ScrollCardCart()
            self.cartcard.ids.cartname.text = y['name']
            self.cartcard.ids.cartprice.text = y['price']
            self.cartcard.ids.cartimage.source = y['image']
            self.cartcard.id = y['itemID']
            self.screen.ids.cart.ids.cartscrollgrid.add_widget(self.cartcard)
        
        for z in self.search: #loading item widgets on the scrollview for search
            self.searchcard = ScrollCard()
            self.searchcard.ids.homename.text =z['name']
            self.searchcard.ids.homeprice.text = str(z['price'])
            self.searchcard.ids.homeimage.source = z['image']
            self.searchcard.id = z['itemID']
            self.screen.ids.search.ids.searchscrollgrid.add_widget(self.searchcard)
            
        for j in self.inventory:
            self.invcard = ScrollCard2()
            self.invcard.ids.invname.text =j['name']
            self.invcard.ids.invprice.text = str(j['price'])
            self.invcard.ids.invimage.source = j['image']
            self.invcard.id = j['itemID']
            self.screen.ids.inventory.ids.inventoryitems.add_widget(self.invcard)
    
    def Android_back_click(self,window,key,*largs):
        if key == 27:
            self.screen.current = 'home'
            return True
           
    def login(self,username,password):
        if username.lower() == "admin" and password == "admin":
            self.screen.current = 'user'
            print("Admin Level")
        else:
            self.screen.current = 'user'
            print("User Level")
    def opennav(self):
        self.screen.ids.nav_id.ids.nav_drawer.set_state("open")
    
    def temprint(self,id):
        print(id)
            
    def clear(self): #clears the cart
        self.screen.ids.cart.ids.cartscrollgrid.clear_widgets() #clear all the widget on the scroll layout
        cart = open('RES/cart.csv', 'w')
        cart.write("itemID,name,price,image,info,stocks,brand\n")
        cart.close() #clears the cart csv file
        
    def delOneItemOnCart(self):
        with open("RES/cart.csv", 'r') as d: #local file that holds the cart items
            self.updateCart = list(DictReader(d))
        print(self.updateCart)
        
    def itemcounter(self,obj,action): #item counter for the cart items
        if (obj.ids.counter.text == '0' and action == -1) is not True:
            obj.ids.counter.text = str(int(obj.ids.counter.text) + action)
        else:
            self.screen.ids.cart.ids.cartscrollgrid.remove_widget(obj)
            self.delOneItemOnCart()
        
    def openitem(self,id):
        self.itemscreen = ItemScreen()
        for x in self.home:
            if x['itemID'] == id:
                self.screen.ids.item.ids.itemID.text = str(x['itemID'])
                self.screen.ids.item.ids.itemname.text = x['name']
                self.screen.ids.item.ids.itemprice.text = str(x['price'])
                self.screen.ids.item.ids.iteminfo.text = x['info']
                self.screen.ids.item.ids.itemimage.source = x['image']
        self.screen.current = 'item'    
            
    def getItem(self,id):
        print(id)
        for x in self.home:
            if x['itemID'] == id:
                return f"{x['itemID']},{x['name']},{x['price']},{x['image']},{x['info']},{x['stocks']},{x['brand']}"  
                      
    def temprint2(self,text):
        print(text)
    
    def addToCart(self,id):
        cart = open('RES/cart.csv', 'a')
        cart.write(f"{self.getItem(id)}\n")
        cart.close()
        self.screen.ids.cart.ids.cartscrollgrid.clear_widgets()
        with open("RES/cart.csv", 'r') as d:
            self.cart = list(DictReader(d))
        for y in self.cart:
            self.cartcard = ScrollCardCart()
            self.cartcard.ids.cartname.text = y['name']
            self.cartcard.ids.cartprice.text = y['price']
            self.cartcard.ids.cartimage.source = y['image']
            self.cartcard.id = y['itemID']
            self.screen.ids.cart.ids.cartscrollgrid.add_widget(self.cartcard)
              
    def build(self):
        return self.screen  
        
if __name__ == '__main__':
    EasyWareApp().run()
