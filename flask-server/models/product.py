from .base import db
from sqlalchemy.dialects.postgresql import ARRAY

class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer,primary_key=True, unique=True)
    title = db.Column(db.String(200))
    size = db.Column(ARRAY(db.String(100)))
    product_detail = db.Column(db.String(200))
    image_url = db.Column(ARRAY(db.String(200)))
    condition = db.Column(db.String(200))
    price = db.Column(db.Integer)
    categories_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    soft_delete = db.Column(db.Boolean, default=False)


    def __init__(self, id: str):
        return self.id == id
    
    def __repr__(self):
        return f"Product(id = {self.id}, name= {self.title})"