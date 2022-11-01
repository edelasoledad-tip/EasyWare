class SudoApp():
    def __init__(self):
        #check update to the firebase
        #if new update is available, update the content of SQLITE db
        #else do nothing
        pass
    
    def get_item(self,item_id): # item_id/INT
        
        # grab item_id on SQLite and returns a formatted json file
        # formatted json {'name':'Allen Key',
        #                 'price':'320.5',
        #                 'image':'RES/RES/allenKey.jpg',
        #                 'info':'Lorem ipsum',
        #                 'stocks':'42',
        #                 'brand':'BondHus'}
        
        pass
    
    def update_item(self,item_id,item_json,user): # item_id/INT, item_json/JSON ,user/BOOL
        
        # updates an item both on the SQLite db if user is admin level
        # logs "item_id updated by user at time" on the user102222log.txt file
        # returns boolean
        
        pass
    
    def delete_item(self,item_id,user): # item_id/INT, user/BOOL
        
        # deletes an item both on the SQLite db if user is admin level
        
        # logs "item_id deleted by user at time" on the user102222log.txt file
        self.log("Erickson","LOG MESSAGE2")
        
        # returns boolean
        
        pass
    
    def insert_item(self,item_id,item_json,user): # item_id/INT, item_json/JSON ,user/BOOL
        
        # insert new item both on the SQLite db if user is admin level
        # logs "item_id inserted by user at time" on the user102222log.txt file
        # returns boolean
        
        pass
    
    def log(self,user,message):
        f = open(f"{user}_log.txt", "a")
        f.write(f"{message}\n")
        f.close()
        
    def update():
        #updates the firebase
        pass
    
    

app = SudoApp()

app.delete_item(5,True)