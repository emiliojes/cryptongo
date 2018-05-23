import requests
import pymongo

API_URL = 'https://api.coinmarketcap.com/v2/ticker/'

def get_db_connection(uri):
	client = pymongo.MongoClient(uri)
	return client.cryptongo

