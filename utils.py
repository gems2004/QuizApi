from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = 'mongodb+srv://georgesalebe:zaq321xsw@cluster0.aerpq12.mongodb.net/?retryWrites=true&w=majority'
# uri = '127.0.0.1:27017'
client = MongoClient(uri,server_api= ServerApi('1'))

try:
    client.admin.command('ping')
    print('Database connected')
except Exception as e:
    print(e)