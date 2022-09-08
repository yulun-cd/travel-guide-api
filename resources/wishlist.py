from flask_restful import Resource, reqparse
from flask_jwt_extended import get_jwt_identity, jwt_required

from models.wishlist import WishlistModel
from helper import city_code_helper, country_code_helper


class Wishlist(Resource):
    
    _wishlist_parser = reqparse.RequestParser()
    _wishlist_parser.add_argument("city_name",
                                  type=str,
                                  required=True,
                                  help="Please enter the name of the city that you wish to visit.")
    _wishlist_parser.add_argument("country_name",
                                  type=str,
                                  required=True,
                                  help="Please enter the name of the country for the city.")
    
    @jwt_required()
    def post(self):
        data = Wishlist._wishlist_parser.parse_args()
        
        city_name, country_name = data['city_name'], data['country_name']
        user_id = get_jwt_identity()

        city_code = city_code_helper(city_name)
        country_code = country_code_helper(country_name)
        if not city_code:
            return {'message': 'Invalid city name.'}, 400
        if not country_code:
            return {'message': 'Invalid country name.'}, 400
        
        wishlist_item = WishlistModel(city_name, city_code, country_name, country_code, user_id)
        
        try:
            wishlist_item.save_to_db()
        except:
            return {'message': 'An error occurred inserting the item.'}, 500
        
        return wishlist_item.json(), 201
    
    @jwt_required()
    def delete(self):
        data = Wishlist._wishlist_parser.parse_args()
        
        city_name, country_name = data['city_name'], data['country_name']
        user_id = get_jwt_identity()

        wishlist_item = WishlistModel.find_by_user_id_and_content(user_id, city_name, country_name)
        if not wishlist_item:
            return {'message': 'Invalid input'}, 400
        wishlist_item.delete_from_db()
        return {'message': 'Successfully deleted'}, 200


class Wishlists(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        
        return {
            'wishlists': [item.json() for item in WishlistModel.find_by_user_id(user_id)]
        }, 200