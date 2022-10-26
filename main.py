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
    
class EasyWareApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen = Builder.load_file('KV/main.kv')
        with open("RES/hardware-products.csv", 'r') as f:
            dict_reader = DictReader(f)
            self.sample = list(dict_reader)
        
        for x in self.sample:
            self.card = ScrollCard()
            self.card.ids.homename.text = x["'name'"].replace("'", "")
            self.card.ids.homeprice.text = x["'price'"].replace("'", "")
            self.card.ids.homeimage.source = x["'image'"].replace("'", "")
            self.screen.ids.home.ids.homescrollgrid.add_widget(self.card)
            
        
    def login(self):
        print(self.screen.ids.login.ids.username.text)
    
    def opennav(self):
        self.screen.ids.nav_id.ids.nav_drawer.set_state("open")
    
    def temprint(self,text):
        for x in self.sample:
            if x["'name'"].replace("'", "") == text:
                print(f"Pressed: {text}")
                
    def build(self):
        return self.screen  
        
if __name__ == '__main__':
    EasyWareApp().run()
