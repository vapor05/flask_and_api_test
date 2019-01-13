import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.item import ItemModel

class Item(Resource):
	parser = reqparse.RequestParser()
	parser.add_argument('price',
		type=float,
		required=True,
		help="This field cannot be left blank"
	)

	@jwt_required()
	def get(self, name):
		item = ItemModel.find_by_name(name)
		if item:
			return item.json(), 200
		return {'message': 'Item not found'}, 200

	@jwt_required()
	def post(self, name):
		if ItemModel.find_by_name(name):
			return {'message': "An item with name '{}' already exists.".format(name)}, 400

		data = Item.parser.parse_args()
		item = ItemModel(name, data['price'])

		try:
			item.insert_new_item()
		except:
			return {'message': 'An error occurred inserting the item'}, 500
		return item.json(), 201

	@jwt_required()
	def delete(self, name):
		if ItemModel.find_by_name(name):
			connection = sqlite3.connect('data.db')
			cursor = connection.cursor()

			delete_query = "DELETE FROM items WHERE name =?"
			cursor.execute(delete_query, (name,))

			connection.commit()
			connection.close()
			return {'message': 'Item deleted'}, 200
		return {'message': "No Item with name '{}' exists".format(name)}, 200

	@jwt_required()
	def put(self, name):
		data = Item.parser.parse_args()

		item = ItemModel.find_by_name(name)
		updated_item = ItemModel(name, data['price'])

		if item is None:
			try:
				updated_item.insert_new_item()
			except:
				return {'message': 'An error occurred inserting the item'}, 500
		else:
			try:
				updated_item.update_row()
			except:
				return {'message': 'An error occurred updating the item'}, 500
		return updated_item.json()


class ItemList(Resource):
	@jwt_required()
	def get(self):
		connection = sqlite3.connect('data.db')
		cursor = connection.cursor()

		all_query = "SELECT * FROM items"
		result = cursor.execute(all_query)
		items = []
		for row in result:
			items.append({'name': row[0], 'price': row[1]})
		return {'items': items}
