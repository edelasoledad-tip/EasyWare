from sudoAPP import FireDataBase
from csv import DictReader


def populateDatabase(MAX=100):
    with open('RES/CSVs/easyware_dataset.csv', 'r', encoding="utf8") as dataFile:
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
if __name__ == '__main__':
    app = FireDataBase()
    
    #populateDatabase()                # populate databae
    #app.addUser('1','Son','123123','RES/Users/son.jpg','Erickson Dela Soledad','Kay Jorayne Lang')
    #app.addUser('1','Zand','123123','RES/Users/zand.jpg','Zandlex Keano Reeves', 'Tambay')
    #app.addUser('1','Nel','123123','RES/Users/nel.jpg',"Ronel German",'Macho Dancer')
    #app.addUser('1','Norvs','123123','RES/Users/norvs.jpg','Arthur Norvy Guzman','OPM Artist')
    #app.addUser('1','Cy','123123','RES/Users/cy.jpg','Cyril Ivan Besagas','Duelist')
    #app.addUser('0','tempUser','123','RES/Users/userProfile.png','Juan Dela Cruz','Cashier')
    #print(app.readItem(12))
    #for x in app.readItem():
        #print(x['itemID'],": ",x['name'])
    
    #print(app.getUser())
    
    #print(app.getUser('Cy'))

    #app.addToCart('Erickson',1)  
    #app.addToCart('Erickson',3) 
    #app.addToCart('Erickson',5) 
    #app.addToCart('Erickson',11)  
    
    #print(app.getUser('Erickson')['fullName'])
    #app.delCart('Erickson',1)
        
    # app.createItem(1, sampleItem)
    # app.updateItem(1000, editedItem)
    # app.deleteItem(11)
    
    #print(app.addToCart('Son',4))
    #print(app.addToCart('tempUser',5))
    #print(app.addToCart('tempUser',6))
    #print(app.addToCart('tempUser',7))
    #print(app.updateUser('tempUser','tempuser','0','Juan Dela Cruz','Cashier 231', '123'))
    
    #print(app.getUser('tempuser'))
    
    #app.delCart('123','7')
    print(app.readItem(20))

