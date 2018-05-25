import requests
import pymongo

API_URL = "https://api.coinmarketcap.com/v1/ticker/"
#API_URL = 'https://api.coinmarketcap.com/v2/ticker/'

def get_db_connection(uri):
	client = pymongo.MongoClient(uri)
	return client.cryptongo

def get_crytocurrencies_from_api():
	r = requests.get(API_URL)
	if r.status_code == 200:
		result = r.json()
		return result

	raise Exception('Api Error')

def get_hash():
	from hashlib import sha512
	return sha512(value.encode('utf-8')).hexdigest()

def first_element(elements):
	return elements[0]	

def get_ticker_hash(ticker_data):
	from collections import OrderedDict
	ticker_data = OrderedDict(
		sorted(
			ticker_data.items(),
			key=first_element
			)
		)
	ticker_value = ''
	for _, value in ticker_data.items():
		ticker_value += str(value)

	return get_hash(ticker_value)

def check_if_exists(db_connection, ticker_data):
	ticker_hash = get_ticker_hash(ticker_data)
	if db_connection.tickers.find_one({'ticker_hash': ticker_hash}):
		return True

	return False

def save_ticket(db_connection, ticker_data=None):
	if not ticker_data:
		return False

	if check_if_exists(db_connection, ticker_data):
		return False

	ticker_hash = get_ticker_hash(ticker_data)
	ticker_data['ticker_hash'] = ticker_hash	
	ticker_data['rank'] = int(ticker_data['rank'])
	ticker_data['last_update'] = int(ticker_data['last_update'])

	db_connection.tickers.insert_one(ticker_data)
	return True

if __name__ == "__main__":
	connection = get_db_connection('mongodb://localhost:27017/')
	tickers = get_crytocurrencies_from_api()

	for ticker in tickers:
		save_ticket(connection, ticker)

	print("Tickers Almacenados")