from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager

from resources.weather import WeatherService
from resources.video import VideoService
from resources.user import User, UserLogin, UserRegister
from resources.wishlist import Wishlist, Wishlists
from resources.journey import Journey, JourneyList

from cache import cache
from db import db


# initialising app
app = Flask(__name__)
app.secret_key = 'koopa'
api = Api(app)

# set up postgresql database
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:zsTTCKMMyM5e2aoa1cOm@containers-us-west-62.railway.app:5622/railway"

# ensure the database is created before first request
@app.before_first_request
def create_tables():
    db.create_all()

# app config
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True

jwt = JWTManager(app)
    
# identify admin
@jwt.additional_claims_loader
def add_claims_to_jwt(identity):
    if identity == 1:
        return {'is_admin': True}
    return {'is_admin': False}
    
# add routes for endpoints
api.add_resource(WeatherService, '/explore/weather/<country>/<city>/<date>')
api.add_resource(VideoService, '/explore/video/<string:city>')

api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserLogin, '/login')
api.add_resource(UserRegister, '/register')
api.add_resource(Wishlist, '/wishlist')
api.add_resource(Wishlists, '/wishlists')
api.add_resource(Journey, '/journey')
api.add_resource(JourneyList, '/journeys')

# start the app
if __name__ == '__main__':
    db.init_app(app)
    cache.init_app(app)
    app.run(port=5000, debug=True)