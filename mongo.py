from pymongo import MongoClient
import urllib.parse

username = urllib.parse.quote_plus('minecraftclyde')
password = urllib.parse.quote_plus('Atlas.database@2004')

cluster = MongoClient(['mongodb+srv://%s:%s@cluster0.kpphkhs.mongodb.net/?ssl=true' % (username, password)])

class db:
    mydb = cluster['database']
    mycol = mydb['apay']
    guild = mydb['prefix']
    play_channel = mydb['player']
    shop = mydb['shop']