from .base import db

class ProductList(db.Model):
    __tablename__ = "product_list"
    details_id = db.Column(db.String(100), db.ForeignKey('product.id'), primary_key=True)
    categories_id = db.Column(db.String(100), db.ForeignKey('categories.id'))

    def __init__(self, id: str):
        return self.details_id = id
    
    def __repr__(self):
        return f"ProductList(item_id = {self.details_id}, categories = {self.categories_id})"