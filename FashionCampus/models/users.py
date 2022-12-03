from .base import db

class Users(db.Model):
    __tablename__ = "users"
    
    id = db.Column(db.Integer, primary_key = True, unique=True)
    token = db.Column(db.String(250))
    nama = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone_number = db.Column(db.String(15))
    password = db.Column(db.String(100))
    balance = db.Column(db.Integer)
    type = db.Column(db.String(100))
    admin = db.Column(db.Boolean())

    def __init__(self, id:str):
        return self.id == id
    
    def __repr__(self):
        return f"Users(id = {self.id}, token = {self.token})"

