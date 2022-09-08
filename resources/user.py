from os import access
from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token

from models.user import UserModel


class UserRegister(Resource):
    
    parser = reqparse.RequestParser()
    parser.add_argument('username', 
                            type=str,
                            required=True, 
                            help='Username required!')
    parser.add_argument('password', 
                            type=str, 
                            required=True,
                            help='Invalid password!')
    parser.add_argument('home',
                            type=str,
                            required=True,
                            help='Home city required!')
    
    def post(self):
        data = UserRegister.parser.parse_args()
        
        if UserModel.find_by_username(data['username']):
            return {'message': 'Username already exists!'}, 400

        user = UserModel(**data)
        user.save_to_db()
        
        return {'message': 'User created successfully'}, 201
    
    
class User(Resource):
    
    def get(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'User not found'}, 404
        return user.json(), 200
    
    
class UserLogin(Resource):
    
    parser = reqparse.RequestParser()
    parser.add_argument('username', 
                            type=str,
                            required=True, 
                            help='Username required!')
    parser.add_argument('password', 
                            type=str, 
                            required=True,
                            help='Invalid password!')
    
    def post(self):
        data = UserLogin.parser.parse_args()
        
        user = UserModel.find_by_username(data['username'])
        
        if not user:
            return {'message': 'Invalid username.'}, 401
        elif user.password != data['password']:
            return {'message': 'Invalid password.'}, 401
        else:
            access_token = create_access_token(identity=user.id)
            return {'access_token': access_token}, 200