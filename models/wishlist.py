from db import db


class WishlistModel(db.Model):
    __tablename__ = 'wishlist'
    
    id = db.Column(db.Integer, primary_key=True)
    city_name = db.Column(db.String(40))
    city_code = db.Column(db.String(3))
    country_name = db.Column(db.String(40))
    country_code = db.Column(db.String(2))
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('UserModel')
    
    def __init__(self, city_name, city_code, country_name, country_code, user_id):
        self.city_name = city_name
        self.city_code = city_code
        self.country_name = country_name
        self.country_code = country_code
        self.user_id = user_id
    
    def json(self):
        return {
            'id': self.id,
            'city_name': self.city_name,
            'city_code': self.city_code,
            'country_name': self.country_name,
            'country_code': self.country_code
        }
        
    @classmethod
    def find_by_user_id(cls, user_id):
        return cls.query.filter_by(user_id=user_id).all()
    
    @classmethod
    def find_by_user_id_and_content(cls, user_id, city_name, country_name):
        return cls.query.filter_by(user_id=user_id, city_name=city_name, country_name=country_name).first()
    
    @classmethod
    def find_by_user_id_and_city_name(cls, user_id, city_name):
        return cls.query.filter_by(user_id=user_id, city_name=city_name).first()
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
        
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()