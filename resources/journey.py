from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity

import re
from helper import flight_price_helper

from models.journey import JourneyModel
from models.user import UserModel
from models.wishlist import WishlistModel


class Journey(Resource):
    
    @jwt_required()
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("name",
                   type=str,
                   required=True, 
                   help="Please enter the name of the journey!")
        
        data = parser.parse_args()
        user_id = get_jwt_identity()
        journey_item = JourneyModel.find_by_name_and_user_id(data['name'], user_id)
        
        if not journey_item:
            return {'message': 'Journey with the name not found'}, 404
        
        return journey_item.json(), 200
    
    @jwt_required()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("name",
                            type=str,
                            required=True,
                            help="Please enter the name of the journey!")
        parser.add_argument("destinations",
                            type=str,
                            action="append",
                            help="Please enter the place(s) you want to visit! (If you are not departuring from or coming back to your home city, you should include the city you wish to departure from or come back to.")
        parser.add_argument("dates",
                            type=str,
                            action="append",
                            help="Please enter your depature date(s) for the place(s) in order. (in the format of YYYY-MM-DD.)")
        parser.add_argument("depart_from_home",
                            type=bool,
                            required=True,
                            help="Please state whether you want to departure from your home city.")
        parser.add_argument("back_home",
                            type=bool,
                            required=True,
                            help="Please state whether you want to come back home at the end of the journey.")
        data = parser.parse_args()
        
        name = data['name']
        user_id = get_jwt_identity()
        
        journey_item = JourneyModel.find_by_name_and_user_id(name, user_id)
        if journey_item:
            return {'message': 'A journey with the name already exists!'}, 400
        
        destinations = data['destinations']
        stops = destinations.copy()
        dates = data['dates']
        home = UserModel.find_by_id(user_id).home
        if data['depart_from_home']:
            destinations.insert(0, home)
        if data['back_home']:
            destinations.append(home)
            
        if len(destinations) - len(dates) != 1:
            return {
                'message': 'Mismatch between destinations and dates. Please check the input.'
            }, 400
        
        cost = 0
        leap_months = [1, 3, 5, 7, 8, 10, 12]
        for i in range(len(dates)):
            date = dates[i]
            if type(date) != str or not re.match("^\d{4}\-\d{2}\-\d{2}$", date):
                return {'message': 'Date not valid! Please check the input.'}, 400
            
            y, m, d = list(map(int, date.split("-")))
            if y < 2022 or m > 12 or (m in leap_months and d > 31) or d > 30:
                return {'message': 'Date not valid! Please check the input.'}, 400
            if type(destinations[i]) != str:
                return {'message': 'Destination not valid! Please check the input.'}, 400
            
            price_to_add = flight_price_helper(destinations[i], destinations[i+1], d, m, y)
            if not price_to_add:
                return {'message': 'Internal error in calculating flight price.'}, 500
            
            wishlist_item = WishlistModel.find_by_user_id_and_city_name(user_id, destinations[i+1])
            if wishlist_item:
                wishlist_item.delete_from_db()
            cost += price_to_add
        
        journey_to_add = JourneyModel(name, cost, stops, user_id)
        journey_to_add.save_to_db()
        return journey_to_add.json(), 201
    
    
class JourneyList(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        
        return {
            'journeys': [item.json() for item in JourneyModel.find_by_user_id(user_id)]
        }, 200