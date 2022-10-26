from csv import DictReader
with open("RES/hardware-products.csv", 'r') as f:
            dict_reader = DictReader(f)
            sample = list(dict_reader)


for x in sample:
    for y in x:
        print(y.replace("'", ""))