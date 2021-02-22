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
app.config['PROPAGATE_EXCEPTIONS'] = True
api = Api(app)

from db import db
db.init_app(app)
migrate = Migrate(app, db, compare_type=True)


if __name__ == '__main__':    
    app.run(port=5000, debug=True)



