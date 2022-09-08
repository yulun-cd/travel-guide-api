from db import db


class UserModel(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))
    home = db.Column(db.String(40))
    
    wishlist = db.relationship('WishlistModel', lazy='dynamic')
    journey = db.relationship('JourneyModel', lazy='dynamic')
    
    def __init__(self, username, password, home):
        self.username = username
        self.password = password
        self.home = home
        
    def json(self):
        return {
            'id': self.id,
            'username': self.username,
            'home': self.home,
            'wishlist': self.wishlist,
            'journey': self.journey
        }
        
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
        
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
        
    @classmethod    
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()
    
    @classmethod    
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()