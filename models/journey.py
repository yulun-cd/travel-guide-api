from db import db


class JourneyModel(db.Model):
    __tablename__ = "journeys"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))
    estimated_cost = db.Column(db.Integer)
    stops = db.Column(db.String(160))
    
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = db.relationship('UserModel')
    
    def __init__(self, name, estimated_cost, stops, user_id):
        self.name = name
        self.estimated_cost = estimated_cost
        self.stops = stops
        self.user_id = user_id
        
    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'estimated_cost': self.estimated_cost,
            'stops': self.stops
        }
        
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
        
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
        
    @classmethod    
    def find_by_name_and_user_id(cls, name, user_id):
        return cls.query.filter_by(name=name, user_id=user_id).first()
    
    @classmethod
    def find_by_user_id(cls, user_id):
        return cls.query.filter_by(user_id=user_id).all()