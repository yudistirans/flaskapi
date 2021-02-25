from db import db
from sqlalchemy import func


class ProductModel(db.Model):
    __tablename__ = 'ms_products'

    product_id = db.Column(db.Integer, primary_key=True)
    product_cd = db.Column(db.String(10))    
    product_slug = db.Column(db.String(500))
    product_name = db.Column(db.String(500))
    product_description = db.Column(db.Text) 
    product_image = db.Column(db.String(500))
    product_price = db.Column(db.Integer)
    product_stock = db.Column(db.Integer)
    created_on = db.Column(db.DateTime)
    updated_on = db.Column(db.DateTime)

    def __init__(self, product_cd, product_slug, product_name, product_description, product_image, product_price, product_stock, created_on, updated_on):
        self.product_cd = product_cd
        self.product_slug = product_slug
        self.product_name = product_name
        self.product_description = product_description
        self.product_image = product_image
        self.product_price = product_price
        self.product_stock = product_stock
        self.created_on = created_on
        self.updated_on = updated_on        

    def json(self):
        return {
            'product_id':self.product_id,
            'product_cd':self.product_cd,
            'product_name':self.product_name,
            'product_description':self.product_description,
            'product_image':self.product_image,
            'product_price':self.product_price,
            'product_stock':self.product_stock,
            'created_on':self.created_on.strftime("%Y-%m-%d %H:%M"),
            'updated_on':self.updated_on.strftime("%Y-%m-%d %H:%M") if self.updated_on else self.updated_on                   
        }    

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, product_id):
        return cls.query.filter_by(product_id=product_id).first()        

    @classmethod
    def find_last_cd(cls):
        return cls.query.order_by(cls.product_cd.desc()).first()

    @classmethod
    def find_by_slug(cls, product_slug):
        return cls.query.filter_by(product_slug=product_slug).first()    

    @classmethod
    def find_by_name(cls, product_name):
        return cls.query.filter(cls.product_name.ilike(product_name)).first()    

    @classmethod
    def find_all(cls):
        return cls.query.order_by(cls.product_id.desc())

