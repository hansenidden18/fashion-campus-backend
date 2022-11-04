from .base import db
from sqlalchemy import func

class Order(db.Model):
    __tablename__ = "order"
    
    id = db.Column(db.Integer, primary_key=True, unique=True)
    time_created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    product = db.Column(db.Integer, db.ForeignKey('product.id'))
    shipping = db.Column(db.String(100))
    shipping_fee = db.Column(db.Integer)
    status = db.Column(db.String(100))
    total_price = db.Column(db.Integer)
    customer_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, id: str):
        return self.id == id
    
    def __repr__(self):
        return f"Order(id = {self.id}, product =  {self.product})"