from flask_restful import Resource, reqparse
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token
from models.user import UserModel

class User(Resource):
    user_parser = reqparse.RequestParser()
    user_parser.add_argument('username', type=str, required=True, help="This field cannot be blank")
    user_parser.add_argument('password', type=str, required=True, help="This field cannot be blank")

    def get(self, id):
        user = UserModel.find_by_id(id)
        if not user:
            return {"message" : "User not found"}, 404
        return user.json(), 200

    def post(self):
        data = User.user_parser.parse_args()
        username = data['username']
        password = generate_password_hash(data['password'])

        if UserModel.find_by_username(username):
            return {'message':'A user that with username already exist'}

        user = UserModel(username, password)
        user.save_to_db()
        return {'message': 'User created successfully'}, 200

class UserLogin(Resource):
    login_parser = reqparse.RequestParser()
    login_parser.add_argument('username', type=str, required=True, help="This field cannot be blank")
    login_parser.add_argument('password', type=str, required=True, help="This field cannot be blank")

    def post(self):
        data = UserLogin.login_parser.parse_args()
        username = data['username']
        password = data['password']

        user = UserModel.find_by_username(username)
        
        if user and check_password_hash(user.password, password):
            access_token = create_access_token(identity=user.username, fresh=True)
            refresh_token = create_refresh_token(user.username)

            return {
                'access_token':access_token,
                'refresh_token':refresh_token
            }, 200
        return {'message': 'Invalid credential'}



