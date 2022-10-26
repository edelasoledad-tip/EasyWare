class database():
    def createItem(self,ITEM):
        # Add item to the database
        return "ITEM ADDED"
    
    def readItem(self,ID):
        # Get json file of an item
        self.giveItemInfo = {
            'ID' : 1,                           # INT ID, unique
            'Name' : 'sample name',             # STRING
            'Price' : 150.69,                   # FLOAT
            'Image' : 'RES/sample_name.png',    # STRING or IMAGE object (for now STRING)
            'Stocks' : 50                       # INT
        }
        return self.giveItemInfo
    
    def updateItem(self,ID,ITEM):
        # Update item info
        self.status = F"Item Updated for ID: {ID}"
        return self.status
    
    def deleteItem(self,ID):
        # Delete item
        return F"ID: {ID} Deleted!"
    
sampleITEM = {
            'ID' : 1,                           # INT ID, unique
            'Name' : 'sample name',             # STRING
            'Price' : 150.69,                   # FLOAT
            'Image' : 'RES/sample_name.png',    # STRING or IMAGE object (for now STRING)
            'Stocks' : 50                       # INT
        }

if __name__ == '__main__':
    db = database()
    print('_'*20+"TEST CASES" +'_'*20, '\n')
    print(db.createItem(sampleITEM),'\n')
    print(db.readItem(1),'\n')
    print(db.updateItem(1,sampleITEM),'\n')
    print(db.deleteItem(1),'\n')