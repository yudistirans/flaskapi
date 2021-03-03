from flask import Flask
from flask_restful import Resource, reqparse
from models.product import ProductModel
import werkzeug, os, uuid, datetime, boto3, botocore
from slugify import slugify

from instance.config import S3_BUCKET_NAME, CLOUDFRONT_LOCATION
from helpers import *

UPLOAD_FOLDER = 'yudistira/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


# API CMS
class Product(Resource):
    def non_empty_string(s):
        if not s:
            raise ValueError()
        return s

    parser = reqparse.RequestParser()
    parser.add_argument('product_id', type=int)
    parser.add_argument('product_name', type=non_empty_string, required=True, help="Product name can not be empty")
    parser.add_argument('product_description', type=non_empty_string, required=True, help="Product description can not be empty")
    parser.add_argument('product_image', type=werkzeug.datastructures.FileStorage, location='files')    
    parser.add_argument('product_price', type=int, required=True, help="Product price can not be empty")
    parser.add_argument('product_stock', type=int, required=True, help="Product stock can not be empty")

    def get(self, product_id = None):
        if product_id != None:
            product = ProductModel.find_by_id(product_id)
            if product:
                return product.json(), 200
            return {'message': 'Product not found'}, 404  
        return [x.json() for x in ProductModel.find_all()], 200

    def post(self):
        data = Product.parser.parse_args()
        product_name = data['product_name']

        is_exist = ProductModel.find_by_name(product_name)
        if is_exist:
            return {'message': "A product with name '{}' already exists.".format(product_name)}, 400              

        last_product = ProductModel.find_last_cd()
        last_product_cd = last_product.product_cd[1:] if last_product else 0
        product_cd = 'P' + str(int(last_product_cd) + 1).zfill(4)

        product_slug = slugify(product_name)
        product_description = data['product_description']         
        product_image = data['product_image']

        if product_image and Product.allowed_file(product_image.filename):
            extension = os.path.splitext(product_image.filename)[1]
            product_image.filename = str(uuid.uuid4()) + extension
            product_image_path = os.path.join(CLOUDFRONT_LOCATION+UPLOAD_FOLDER,product_image.filename)
            upload_file_to_s3(product_image, S3_BUCKET_NAME, UPLOAD_FOLDER)
        else:
            return {"message": "Image can not be empty and check your format image!"}, 400           
        
        product_price = data['product_price']
        product_stock = data['product_stock'] 
        created_on = datetime.datetime.now()

        product = ProductModel(product_cd, product_slug, product_name, product_description, product_image_path, product_price, product_stock, created_on, None)
        
        try:
            product.save_to_db()
        except:
            return {"message": "An error occurred inserting the product."}, 500

        return product.json(), 201

    def delete(self, product_id):
        product = ProductModel.find_by_id(product_id)
        if product:
            product.delete_from_db()
            return {'message': 'Product deleted'}, 200
        return {'message': 'Product not found.'}, 404

    def put(self):
        data = Product.parser.parse_args() 

        product_id = data['product_id']
        product_name = data['product_name']   
        product_slug = slugify(product_name)        
        product_description = data['product_description']
        product_image = data['product_image']  
        product_price = data['product_price']
        product_stock = data['product_stock']
        updated_on = datetime.datetime.now()
        
        is_exist = ProductModel.find_by_name(product_name)
        if is_exist and is_exist.product_id != product_id:
            return {'message': "A product with name '{}' already exists.".format(product_name)}, 400           

        product = ProductModel.find_by_id(product_id)

        if product:
            product_image_path = product.product_image
            
            product.product_name = product_name
            product.product_slug = product_slug
            product.product_description = product_description            

            if product_image:
                if Product.allowed_file(product_image.filename):
                    remove_file_from_s3(product.product_image.split("/")[-1], S3_BUCKET_NAME, UPLOAD_FOLDER)
                
                    extension = os.path.splitext(product_image.filename)[1]
                    product_image.filename = str(uuid.uuid4()) + extension
                    product_image_path = os.path.join(CLOUDFRONT_LOCATION+UPLOAD_FOLDER,product_image.filename)
                    upload_file_to_s3(product_image, S3_BUCKET_NAME, UPLOAD_FOLDER)
                    
                    product.product_image = product_image_path    
                else:
                    return {"message": {'image': 'Image allowed filetypes : png,jpeg,jpg'}}, 400               
            
            product.product_price = product_price
            product.product_stock = product_stock
            product.updated_on = updated_on

            product.save_to_db()

            return product.json(), 201
        else:
            return {'message': 'Product not found'}

    @classmethod
    def allowed_file(cls, filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# API Public Site
class ProductSlug(Resource):
    def get(self, product_slug):
        product = ProductModel.find_by_slug(product_slug)
        if product:
            return  product.json(), 200
        return {'message': 'Product not found'}, 404  

class ProductList(Resource):
    def get(self):
        return [x.json() for x in ProductModel.find_all()], 200