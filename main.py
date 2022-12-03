from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.core.text import LabelBase
from kivy.properties import StringProperty
from kivymd.uix.card import MDCard
from sudoAPP import FireDataBase
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.menu import MDDropdownMenu
from kivymd.toast import toast

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
        self.dialog = None
        self.searchByFilter = 'name'
        menu_items = [
            {
                "text": f"{i}",
                "viewclass": "OneLineListItem",
                'font_size': 1,
                'height': 60,
                'size_hint_y': None,
                "on_release": lambda x = f"{i}": self.set_item(x),
            } for i in ["Name","Price ASC","Price DSC", "Brand"]
        ]
        self.menu = MDDropdownMenu(
            caller=self.screen.ids.home.ids.sort,
            items=menu_items,
            width_mult = 2.5, 
        )
        self.menu2 = MDDropdownMenu(
            caller=self.screen.ids.searchAdmin.ids.sort,
            items=menu_items,
            width_mult = 2.5, 
        )
        search_items = [
            {
                "text": f"{i}",
                "viewclass": "OneLineListItem",
                'font_size': 1,
                'height': 50,
                'size_hint_y': None,
                "on_release": lambda x = f"{i}": self.set_search(x),
            } for i in ["Name","Price", "Brand"]
        ]
        self.searchby = MDDropdownMenu(
            caller=self.screen.ids.search.ids.searchBy,
            items=search_items,
            width_mult = 2.5, 
        )
        
    def set_search(self,x):
        self.screen.ids.search.ids.searchByLbl.text = x
        self.searchByFilter = x.lower()
        self.searchby.dismiss() 
    
    def set_item(self,x):
        self.screen.ids.home.ids.sortBy.text = x
        self.screen.ids.searchAdmin.ids.sortBy.text = x
        try:
            print("working")
            if x == "Name":
                self.items = self.backEnd.readItem(0,1)
            elif x == "Price DSC":
                self.items = self.backEnd.readItem(0,3)
            elif x == "Price ASC":
                self.items = self.backEnd.readItem(0,4)
            else:
                self.items = self.backEnd.readItem(0,2)
        except:
            pass
        self.reloadAll()
        self.menu.dismiss() 
        self.menu2.dismiss() 
          
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
            self.error('Incorrect Username or Password')
            
    def error(self,message):
        self.dialog = MDDialog(
        text= message,
        elevation = 0)
        self.dialog.open()
        self.dialog = None
            
    def search(self,text):      #Search function for recycle view  
        holder = [{  'image': y['image'],'name': y['name'],'price': str(y['price']), 'id': str(y['itemID'])} for y in self.items if text.lower() in str(y[self.searchByFilter]).lower()]
        self.screen.ids.search.ids.searchrecycleview.data = holder
        self.screen.ids.searchAdmin.ids.searchrecycleview.data = holder
    
    def reloadAll(self):           #Reloads item from database
        try:
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
        except:
            print('error on reload all')
         
    def reloadCart(self):           #Reloads the cart items
        try:
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
        except:
            print('error on reload cart')
    
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
    
    def checkOutCnfrm(self,obj):
        total = 0
        try:
            for x in self.cart:
                total += float(x['price'])*int(x['quantity'])
                self.screen.ids.checkout.ids.subtotal.text = str(round(total,2))
                self.backEnd.invoice(self.username)
                toast('Invoice generated!')
        except:
            self.screen.ids.checkout.ids.subtotal.text = '0'
            print('empty cart')
        self.screen.current = 'checkout'
        self.dialog.dismiss()
        self.dialog = None
        
    def checkOut(self): 
        if self.cart == False:
            toast('Empty Cart')   
        else:
            if not self.dialog:
                self.dialog = MDDialog(
                    title ="[font=RES/fonts/BebasNeue-Regular.otf]Continue CheckOut?[/font]",
                    text="[font=RES/fonts/BebasNeue-Regular.otf]Items will be removed after checkout![/font]",
                    elevation = 0,
                    buttons=[
                        MDFlatButton(
                            text="CANCEL",
                            size_hint = (.5, .75),
                            font_name = 'Nunito',
                            md_bg_color = 'ec8c6f',
                            theme_text_color="Custom",
                            text_color= (1,1,1,1),
                            on_release = self.closeDiag,
                        ),
                        MDFlatButton(
                            text="CONTINUE",
                            size_hint = (.5, .75),
                            font_name = 'Nunito',
                            md_bg_color = 'ec8c6f',
                            theme_text_color="Custom",
                            text_color= (1,1,1,1),
                            on_release = self.checkOutCnfrm,
                            
                        ),
                    ],
                )
            self.dialog.open()
    
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
        self.screen.current = 'home'
        try:
            self.backEnd.addToCart(self.username,itemID)
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
            if editedItem == self.backEnd.readItem(int(item['itemID'])):
                toast('No Changes!')
            else:
                self.backEnd.updateItem(int(item['itemID']), editedItem)
                toast('Item Details Saved!')
                self.screen.current = 'homeAdmin'
        except:
            pass
        self.items = self.backEnd.readItem()
        self.reloadAll()
    
    def addItem(self,itemDetails):
        try:
            if "" in itemDetails.values():
                toast("Please Fill All Fields!")
            else:
                self.backEnd.createItem(self.backEnd.getNewItemID(),itemDetails)
                self.screen.ids.itemAdd.ids.itemBrand.text = ""
                self.screen.ids.itemAdd.ids.itemColor.text = ""
                self.screen.ids.itemAdd.ids.itemInfo.text = ""
                self.screen.ids.itemAdd.ids.itemName.text = ""
                self.screen.ids.itemAdd.ids.itemPrice.text = ""
                self.screen.ids.itemAdd.ids.itemStocks.text = ""
                self.screen.ids.itemAdd.ids.itemType.text = ""
                toast('Item Added')
                self.screen.current = 'homeAdmin'
        except:
            print('something went wrong')
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
            bck = self.backEnd.getUser(user['userName'])
            if (user['updatedUserName'],user['password'],user['fName'],user['position'],str(int(user['accType']))) == (bck['username'],bck['password'],bck['fullName'],bck['position'],bck['accountType']):
                toast('No Changes!')
            else:
                self.backEnd.updateUser(user['userName'],
                                        user['updatedUserName'],
                                        str(int(user['accType'])),
                                        user['fName'],
                                        user['position'],
                                        user['password'])
                toast('Changes Saved!')
                self.screen.current = 'usersAdmin'
        except:
            pass
        self.reloadAll()
    
    def deleteUser(self,userName):
        try:
            self.backEnd.delUser(userName)
            toast('Success!')
        except:
            pass
        self.reloadAll()
    
    def addUser(self,user):
        try:
            if "" in user.values():
                toast('Please Fill All Fields')
            else:
                self.backEnd.addUser(str(int(user['accType'])),user['userNameInput'],user['password'],'RES/Users/userProfile.png',user['fName'],user['position'])
                toast(f"{user['userNameInput']} Added")
                self.screen.ids.userAdd.ids.userNameInput.text = ""
                self.screen.ids.userAdd.ids.userType.active = False
                self.screen.ids.userAdd.ids.fullNameInput.text = ""
                self.screen.ids.userAdd.ids.positionInput.text = ""
                self.screen.ids.userAdd.ids.passwordInput.text = ""
                self.screen.current = 'usersAdmin'
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
    
    def deleteAllCartCnfrm(self,obj):
        try:
            self.backEnd.delCart(self.username)
            toast('Cart Cleared!')
        except:
            pass
        self.reloadCart()
        self.dialog.dismiss()
        self.dialog = None
    
    def deleteAllCart(self):
        if not self.dialog:
            self.dialog = MDDialog(
                text="[font=RES/fonts/BebasNeue-Regular.otf]Delete All Items?[/font]",
                elevation = 0,
                buttons=[
                    MDFlatButton(
                        text="CANCEL",
                        size_hint = (.5, .75),
                        font_name = 'Nunito',
                        md_bg_color = 'ec8c6f',
                        theme_text_color="Custom",
                        text_color= (1,1,1,1),
                        on_release = self.closeDiag,
                    ),
                    MDFlatButton(
                        text="CONTINUE",
                        size_hint = (.5, .75),
                        font_name = 'Nunito',
                        md_bg_color = 'ec8c6f',
                        theme_text_color="Custom",
                        text_color= (1,1,1,1),
                        on_release = self.deleteAllCartCnfrm,
                        
                    ),
                ],
            )
        self.dialog.open()
        
    def closeDiag(self,obj):
        self.dialog.dismiss()
        self.dialog = None
     
    def build(self):
        return self.screen  

if __name__=="__main__":
    EasyWare().run()