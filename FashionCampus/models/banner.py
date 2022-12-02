from .base import db

class Banner(db.Model):
    __tablename__ = 'banner'

    id = db.Column(db.Integer,primary_key=True, unique=True)
    image_url = db.Column(db.String(200))
    title = db.Column(db.String(100))

    def __init__(self, id: str):
        return self.id == id
    
    def __repr__(self):
        return f"Banner(image_url= {self.image_url}, title={self.title})"