import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

class Item(Resource):
	parser = reqparse.RequestParser()
	parser.add_argument('price',
		type=float,
		required=True,
		help="This field cannot be left blank"
	)

	@jwt_required()
	def get(self, name):
		item = self.find_by_name(name)
		if item:
			return item, 200
		return {'message': 'Item not found'}, 200

	@classmethod
	def find_by_name(cls, name):
		connection = sqlite3.connect('data.db')
		cursor = connection.cursor()

		select_query = "SELECT * FROM items WHERE name=?"
		result = cursor.execute(select_query, (name,))
		row = result.fetchone()
		connection.close()

		if row:
			return {'item': {'name': row[0], 'price': row[1]}}

	@classmethod
	def insert_new_item(cls, name, price):
		connection = sqlite3.connect('data.db')
		cursor = connection.cursor()

		insert_query = "INSERT INTO items VALUES (?, ?)"
		cursor.execute(insert_query,(name, price))

		connection.commit()
		connection.close()

	@classmethod
	def update_row(cls, item):
		connection = sqlite3.connect('data.db')
		cursor = connection.cursor()

		update_query = "UPDATE items SET price=? WHERE name=?"
		cursor.execute(update_query, (item['price'], item['name']))

		connection.commit()
		connection.close()

	def post(self, name):
		if self.find_by_name(name):
			return {'message': "An item with name '{}' already exists.".format(name)}, 400

		data = Item.parser.parse_args()
		item = {'name': name, 'price': data['price']}

		try:
			self.insert_new_item(item['name'], item['price'])
		except:
			return {'message': 'An error occurred inserting the item'}, 500
		return item, 201

	def delete(self, name):
		if self.find_by_name(name):
			connection = sqlite3.connect('data.db')
			cursor = connection.cursor()

			delete_query = "DELETE FROM items WHERE name =?"
			cursor.execute(delete_query, (name,))

			connection.commit()
			connection.close()
			return {'message': 'Item deleted'}, 200
		return {'message': "No Item with name '{}' exists".format(name)}, 200

	def put(self, name):
		data = Item.parser.parse_args()
		item = {'name': name, 'price': data['price']}

		if self.find_by_name(name) is None:
			try:
				self.insert_new_item(item['name'], item['price'])
			except:
				return {'message': 'An error occurred inserting the item'}, 500
		else:
			try:
				self.update_row(item)
			except:
				return {'message': 'An error occurred updating the item'}, 500
		return item

class ItemList(Resource):
	def get(self):
		connection = sqlite3.connect('data.db')
		cursor = connection.cursor()

		all_query = "SELECT * FROM items"
		result = cursor.execute(all_query)
		items = []
		for row in result:
			items.append({'name': row[0], 'price': row[1]})
		return {'items': items}
