from csv import DictReader

def cleanCSV():
    with open('RES/item_details.csv','r') as dataFile:
        i = 1
        temp = DictReader(dataFile)
        sample = list(temp)
        newDict = {}
        for data in sample:
            for entry in data:
                newDict[entry.replace("'","")] = data[entry].replace("'","")
            print("-----------\n-----------")
            print(f"Entry number {i}")
            for key in newDict:
                print(f"{key}: {newDict[key]} ")
            i+=1    
               

cleanCSV()