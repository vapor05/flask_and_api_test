from flask import Flask, jsonify, request

app = Flask(__name__)

stores = [
	{
		'name':'My Wonderful Store',
		'items': [
			{
			'name': 'My Item',
			'price': 15.99
			}
		]
	}
]

# POST - used to receive data
# GET - used to send data back only

# POST /store data: {name:}
@app.route('/store', methods=['POST'])
def create_store():
	# Receive request data
	# Iterate over stores
	# If the store name matches, add request data to the stores store dict list
	# Else, return an error message
	request_data = request.get_json()
	new_store = {
		'name': request_data['name'],
		'items': []
	}
	stores.append(new_store)
	return jsonify(new_store)
	
# GET /store data: {name:}
@app.route('/store/<string:name>') # 'http://127.0.0.1:5000/store/some_name'
def get_store(name):
	# Iterate over stores
	# If the store name matches, return it
	# Else, return an error message
	for store in stores:
		if store['name'] == name:
			return jsonify(store)
	return jsonify({'message': 'Store not found'})
	
# GET /store
@app.route('/store')
def get_stores():
	# Just return the whole stores dict
	return jsonify({'stores': stores})
	
# POST /store/<string:name>/item {name:, price:}
@app.route('/store/<string:name>/item', methods=['POST'])
def create_item_in_store(name):
	# Receive request data
	# Iterate over stores
	# If the store name matches, add request data to the store's item dict list
	# Else, return an error message
	request_data = request.get_json()
	for store in stores:
		if store['name'] == name:
			new_item = {
				'name': request_data['name'],
				'price': request_data['price']
			}
			store['items'].append(new_item)
			return jsonify(new_item)
	return jsonify({'message': 'store not found'})
				
# GET /store/<string:name>/item'
@app.route('/store/<string:name>/item')
def get_items_in_store(name):
	# Iterate over stores
	# If the store name matches, return its items list contents (dictionaries)
	# Else, return an error message
	for store in stores:
		if store['name'] == name:
			return jsonify({'items': store['items']})
	return jsonify({'message': 'store not found'})
	
app.run(port=5000)
