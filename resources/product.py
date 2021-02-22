from flask import Flask, jsonify, request
from flask_restful import Resource, reqparse
from models.product import ProductModel
import werkzeug, os, uuid, datetime, boto3, botocore
from slugify import slugify

class Product(Resource):
    def non_empty_string(s):
        if not s:
            raise ValueError()
        return s

    parser = reqparse.RequestParser()
    parser.add_argument('product_id', type=int)
    parser.add_argument('product_name', type=non_empty_string, required=True, help="Name can not be empty")
    parser.add_argument('product_description', type=non_empty_string, required=True, help="Name can not be empty")
    parser.add_argument('product_image', type=werkzeug.datastructures.FileStorage, location='files')    

    def get(self, product_id):
        product = ProductCategoryModel.find_by_id(product_id)
        if product:
            return {
                'product': product.json()
            }, 200
        return {'message': 'Product not found'}, 404  

    def post(self):
        pass

    def delete(self, cd):
        pass

    def put(self):
        pass

    @classmethod
    def allowed_file(cls, filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

class ProductSlug(Resource):
    def get(self, slug):
        pass

class ProductList(Resource):
    def get(self):
        pass