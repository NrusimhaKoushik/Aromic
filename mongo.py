from pymongo import MongoClient

cluster = MongoClient('YOUR_MONGO_CONNECTION_URL')

class db:
    mydb = cluster['database']
    mycol = mydb['apay']
    guild = mydb['prefix']
    play_channel = mydb['player']
    shop = mydb['shop']
