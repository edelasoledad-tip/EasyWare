from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.core.text import LabelBase
from kivy.uix.floatlayout import FloatLayout
from kivymd.uix.card import MDCard
from kivy.properties import ObjectProperty
from csv import DictReader
# open file in read mode


Window.size = (270, 550)
LabelBase.register(name = "Nunito", fn_regular= "RES/BebasNeue-Regular.otf")

class ScrollCard(MDCard):
    pass
class ScrollCardCart(MDCard):
    pass
class EasyWareApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen = Builder.load_file('KV/main.kv')
        
        self.cart = [{'pos': '1',
                      'name':'Allen Key',
                      'price':'320.5',
                      'image':'RES/RES/allenKey.jpg',
                      'info':'Lorem ipsum dolor sit amet. Consectetur adipiscing elit. Lorem ipsum Dolor sit amet Sed ut perspiciatis',
                      'stocks':'42',
                      'brand':'BondHus'},
                     {'pos': '2',
                     'name':'Band Clamp',
                      'price':'793.1',
                      'image':'RES/RES/bandClamp.jpg',
                      'info':'Lorem ipsum dolor sit amet. Consectetur adipiscing elit. Lorem ipsum Dolor sit amet Sed ut perspiciatis',
                      'stocks':'44',
                      'brand':'Generic'},
                     {'pos': '3',
                     'name':'Cable Cutter',
                      'price':'119.5',
                      'image':'RES/RES/cableCutter.jpg',
                      'info':'Lorem ipsum dolor sit amet. Consectetur adipiscing elit. Lorem ipsum Dolor sit amet Sed ut perspiciatis',
                      'stocks':'35',
                      'brand':'Stanley'},
                     {'pos': '4',
                     'name':'Bricks',
                      'price':'10.5',
                      'image':'RES/RES/bricks.jpg',
                      'info':'Lorem ipsum dolor sit amet. Consectetur adipiscing elit. Lorem ipsum Dolor sit amet Sed ut perspiciatis',
                      'stocks':'6',
                      'brand':'ABC'},
                     {'pos': '5',
                     'name':'Cement',
                      'price':'227.8',
                      'image':'RES/RES/cement.jpg',
                      'info':'Lorem ipsum dolor sit amet. Consectetur adipiscing elit. Lorem ipsum Dolor sit amet Sed ut perspiciatis',
                      'stocks':'19',
                      'brand':'Generic'}]
        
        with open("RES/item_details.csv", 'r') as f:
            self.home = list(DictReader(f))
        with open("RES/item_details.csv", 'r') as g:
            self.search = list(DictReader(g))
        
        for x in self.home:
            self.card = ScrollCard()
            self.card.ids.homename.text = x['name']
            self.card.ids.homeprice.text = x['price']
            self.card.ids.homeimage.source = x['image']
            self.screen.ids.home.ids.homescrollgrid.add_widget(self.card)
        
        for y in self.cart:
            self.cartcard = ScrollCardCart()
            self.cartcard.ids.cartname.text = y['name']
            self.cartcard.ids.cartprice.text = y['price']
            self.cartcard.ids.cartimage.source = y['image']
            self.screen.ids.cart.ids.cartscrollgrid.add_widget(self.cartcard)
        
        for z in self.search:
            self.searchcard = ScrollCard()
            self.searchcard.ids.homename.text =z['name']
            self.searchcard.ids.homeprice.text = z['price']
            self.searchcard.ids.homeimage.source = z['image']
            self.screen.ids.search.ids.searchscrollgrid.add_widget(self.searchcard)
        
    def login(self,username,password):
        if username.lower() == "admin" and password == "admin":
            self.screen.current = 'user'
            print("Admin Level")
        else:
            self.screen.current = 'user'
            print("User Level")
    def opennav(self):
        self.screen.ids.nav_id.ids.nav_drawer.set_state("open")
    
    def temprint(self,text):
        for x in self.home:
            if x['name'] == text:
                print(f"Pressed: {text}")
                print("INFO: ",x['info'])
                print("BRAND: ",x['brand'])
            
    def clear(self):
        rows = [i for i in self.screen.ids.cart.ids.cartscrollgrid.children]
        for row in rows:
            self.screen.ids.cart.ids.cartscrollgrid.remove_widget(row)
        self.cart = []
    
    def itemcounter(self,str):
        print(str)
            
                
    def temprint2(self,text):
        print(text)
                
    def build(self):
        return self.screen  
        
if __name__ == '__main__':
    EasyWareApp().run()
