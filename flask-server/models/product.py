from .base import db
from sqlalchemy.dialects.postgresql import ARRAY

class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.String(100),primary_key=True, nullable=True)
    title = db.Column(db.String(200))
    brand_name = db.Column(db.String(200))
    size = db.Column(ARRAY(db.String(100)))
    product_detail = db.Column(db.String(200))
    image_url = db.Column(db.String(200))
    condition = db.Column(db.String(200))
    price = db.Column(db.Integer)
    categories_id = db.Column(db.String(100), db.ForeignKey('categories.id'))

    def __init__(self, id: str):
        return self.id = id
    
    def __repr__(self):
        return f"Product(id = {self.id}, name= {self.title})"