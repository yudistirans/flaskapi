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
    created_on = db.Column(db.DateTime)
    updated_on = db.Column(db.DateTime)

    def __init__(self, product_cd, product_slug, product_name, product_description, product_image, created_on, updated_on):
        self.product_cd = product_cd
        self.product_slug = product_slug
        self.product_name = product_name
        self.product_description = product_description
        self.product_image = product_image
        self.created_on = created_on
        self.updated_on = updated_on        

    def json(self):
        return {
            'product_id':self.product_id,
            'product_cd':self.product_cd,
            'product_name':self.product_name,
            'product_description':self.product_description,
            'product_image':self.product_image,
            'image_icon':self.image_icon,
            'created_on':self.created_on.strftime("%Y-%b-%d %X"), 
            'created_on_disp':self.created_on.strftime("%Y-%m-%d %H:%M"),
            'updated_on':self.updated_on.strftime("%Y-%b-%d %X") if self.updated_on else self.updated_on,
            'updated_on_disp':self.updated_on.strftime("%Y-%m-%d %H:%M") if self.updated_on else self.updated_on                   
        }    

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).filter(cls.status!='deleted').first()    

    @classmethod
    def find_by_cd(cls, cd, lang):
        return cls.query.filter_by(product_category_cd=cd).filter_by(language=lang).filter(cls.status!='deleted').first()

    @classmethod
    def find_last_id(cls):
        return cls.query.order_by(cls.id.desc()).first()

    @classmethod
    def find_last_cd(cls):
        return cls.query.order_by(cls.product_category_cd.desc()).first()

    @classmethod
    def find_by_slug(cls, slug):
        return cls.query.filter_by(slug=slug).filter(cls.status!='deleted').first()    

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter(cls.name.ilike(name)).filter(cls.status!='deleted').first()    

    @classmethod
    def find_all(cls):
        return cls.query.filter(cls.status!='deleted').order_by(cls.order.asc())

