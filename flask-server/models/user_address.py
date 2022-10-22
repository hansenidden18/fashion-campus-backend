from .base import db

class User_Address(db.Model):
    __tablename__ = 'user_address'
    id = db.Column(db.String(100),primary_key=True, nullable=False)
    user_id = db.Column(db.String(100), db.ForeignKey('users.id'))
    name = db.Column(db.String(200))
    phone_number = db.Column(db.Integer())
    address = db.Column(db.String(100))
    city = db.Column(db.String(100))

    def __init__(self, id: str):
        return self.id == id
    
    def __repr__(self):
        return f"Product(id = {self.id}, user= {self.user_id})"

