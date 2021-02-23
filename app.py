from flask import Flask, jsonify
from flask_restful import Api
from flask_migrate import Migrate
from flask_cors import CORS

# Product Resource
from resources.product import Product, ProductSlug, ProductList

app = Flask(__name__, instance_relative_config=True)
CORS(app, resources={r"/*": {"origins": ["http://localhost:3000"]}})
app.config.from_pyfile('config.py')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

api = Api(app)

from db import db
db.init_app(app)
migrate = Migrate(app, db, compare_type=True)

# Product category route
product_routes = [
    '/product',
    '/product/<string:product_id>',
]
api.add_resource(Product, *product_routes)
api.add_resource(ProductSlug, '/api/product/<string:product_slug>')
api.add_resource(ProductList, '/api/products')

if __name__ == '__main__':    
    app.run(port=5000, debug=True)



