import pyrebase
import os


firebaseConfig = {
  "apiKey": "AIzaSyCw5R8aXhVZC1PCQ9Ec0_0WXAxYGZvPPGc",
  "authDomain": "easywareph-2f473.firebaseapp.com",
  "databaseURL": "https://easywareph-2f473-default-rtdb.asia-southeast1.firebasedatabase.app/",
  "projectId": "easywareph-2f473",
  "storageBucket": "easywareph-2f473.appspot.com",
  "messagingSenderId": "107477791479",
  'appId': "1:107477791479:web:903a72384bb70778a419f2",
  "measurementId": "G-Y2VJLX01KS",
  "serviceAccount": "keyServiceAccount.json"
}

storageLink = "https://console.firebase.google.com/project/easywareph-2f473/storage/easywareph-2f473.appspot.com/files"

firebase = pyrebase.initialize_app(firebaseConfig)
fstg = firebase.storage()


downloadDirectory = "sampleDirectory/"
inputFolder = "sampleInputDirectory/"

def downloadAllFiles(folder):
    storageFiles = fstg.list_files()
    # if not os.path.exists(folder):
    #     os.makedirs(folder)
    # need to initialize folder
    for file in storageFiles:
        print(file.name)
        file.download_to_filename(folder + file.name)
def uploadFiles(source):
    fstg.child(source).put(source)
