import pymongo
import os

client = pymongo.MongoClient(host='127.0.0.1', port=27017)
db = client.anonymous_telegram_bot
