from .base import db
from sqlalchemy.dialects.postgresql import ARRAY

class Cart(db.Model):
    __tablename__ = "cart"
    
    id = db.Column(db.Integer, primary_key=True, unique=True)
    quantity = db.Column(db.Integer)
    size = db.Column(ARRAY(db.String(100)))
    price = db.Column(db.Integer)
    image = db.Column(db.String(100))
    name = db.Column(db.Integer, db.ForeignKey('product.id'))
    customer_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, id: str):
        return self.id == id
    
    def __repr__(self):
        return f"Cart(id = {self.id}, name = {self.name})"
