from sudoAPP import FireDataBase
from csv import DictReader


def populateDatabase(MAX=1000):
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
    
    populateDatabase()                # populate databae
    
    
    for x in app.readItem():
        print(x)
        
        
    # app.createItem(1, sampleItem)
    # app.updateItem(1000, editedItem)
    # app.deleteItem(11)
