from .base import db
from sqlalchemy.dialects.postgresql import ARRAY

class Cart(db.Model):
    __tablename__ = "cart"
    
    id = db.Column(db.String(100), primary_key=True, nullable=False)
    quantity = db.Column(db.Integer)
    size = db.Column(ARRAY(db.String(100)))
    price = db.Column(db.Integer)
    image = db.Column(db.String(100))
    name = db.Column(db.String(100), db.ForeignKey('product.id'))

    def __init__(self, id: str):
        return self.id == id
    
    def __repr__(self):
        return f"Cart(id = {self.id}, name = {self.name})"
