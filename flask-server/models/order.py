from .base import db
from sqlalchemy import func

class Order(db.model):
    __tablename__ = "order"
    
    id = db.Column(db.String(100), primary_key=True, nullable=False)
    time_created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    product = db.Column(db.String(100), db.ForeignKey('product.id'))
    shipping = db.Column(db.String(100))
    shipping_fee = db.Column(db.Integer)
    status = db.Column(db.String(100))
    total_price = db.Column(db.Integer)
    customer_id = db.Column(db.String(100), db.ForeignKey('users.id'))