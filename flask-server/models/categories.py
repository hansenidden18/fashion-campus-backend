from .base import db

class Categories(db.Model):
    __tablename__ = "categories"
    
    id = db.Column(db.Integer, primary_key = True, unique=True)
    title = db.Column(db.String(200))

    def __init__(self, id:str):
        return self.id == id
    
    def __repr__(self):
        return f"Categories(id = {self.id}, title = {self.title})"