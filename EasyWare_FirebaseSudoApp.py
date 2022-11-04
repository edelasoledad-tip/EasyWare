import pyrebase,json,requests,json
from asyncore import read
from csv import DictReader
from traceback import format_list


firebaseConfig = {
  "apiKey": "AIzaSyCw5R8aXhVZC1PCQ9Ec0_0WXAxYGZvPPGc",
  "authDomain": "easywareph-2f473.firebaseapp.com",
  "databaseURL": "https://easywareph-2f473-default-rtdb.asia-southeast1.firebasedatabase.app/",
  "projectId": "easywareph-2f473",
  "storageBucket": "easywareph-2f473.appspot.com",
  "messagingSenderId": "107477791479",
  'appId': "1:107477791479:web:903a72384bb70778a419f2",
  "measurementId": "G-Y2VJLX01KS"
}
firebase = pyrebase.initialize_app(firebaseConfig)
fdb = firebase.database()
def populateDatabase():
    with open('RES/item_details.csv','r') as dataFile:
        i = 1
        temp = DictReader(dataFile)
        sample = list(temp)
        newDict = {}
        for data in sample:
            for entry in data:
                newDict[entry.replace("'","")] = data[entry].replace("'","")
            print(db.createItem(i,newDict))
            i+=1




class database():
        
    def createItem(self,itemID,ITEM):
        fdb.child("items").child(itemID).set(ITEM)
        return f"Added item with Id of {itemID}"
    
    def readItem(self,ID):
        temp = fdb.child("items").child(ID).get()
        return {
            'id':temp.val()['id'],
            'name':temp.val()['name'],
            'price':temp.val()['price'],
            'stocks':temp.val()['stocks'],
            'image':temp.val()['image'],
            'info':temp.val()['info']}
    def readAllItems(self):
        items = fdb.child("items").get()
        for item in items.each():
            if item.val() is not None:
                print(item.key(),":",item.val())
        return '----Shown all items----'
    
    def updateItem(self,ID,ITEM):
        fdb.child("items").child(ID).update(ITEM)
        self.status = F"Item Updated for ID: {ID}"
        return self.status
    
    def deleteItem(self,ID):
        fdb.child("items").child(ID).remove()
        return F"ID: {ID} Deleted!"

if __name__ == '__main__':
    db = database()
    # print('_'*20+"TEST CASES" +'_'*20, '\n')
    # print(db.createItem(sampleITEM),'\n')
    # print(db.createItem(sampleITEM2),'\n')
    # print(db.createItem(sampleITEM3),'\n')
    # print(db.readItem(3),'\n')
    # print(db.readAllItems())
    # print(db.updateItem(2,editedItem),'\n')
    # print(db.readItem(2),'\n')
    #print(db.deleteItem(1),'\n')
    # print(db.readAllItems())
    # print(db.createItem(sampleITEM4),'\n')
    # print(db.readItem(2))
    # item = fdb.child("items").get()
    # for items in item.each():
    #         if item.val() is not None:
    #             print(item.key())
    # populateDatabase()    
    print(db.readAllItems())
