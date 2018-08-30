from flask import Blueprint, request, Response, jsonify, make_response
from flask_restful import Resource,Api
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity, JWTManager
from my_api.models.dbase import DatabaseConnection
import json
import validators
from werkzeug.security import check_password_hash
from datetime import timedelta

auth_blueprint = Blueprint('auth', __name__, url_prefix='/api/v1')
api = Api(auth_blueprint)
database_connection = DatabaseConnection()


class QuestionsBox(Resource):
    @jwt_required
    def get(self):
        current_user = get_jwt_identity()
        if current_user:
            question_dict = database_connection.get_all_questions()
            if question_dict:
                return make_response(jsonify(question_dict), 200)
        return Response(json.dumps(['No questions to display!']), status=404, mimetype='application/json')

    def post(self):
            data = request.get_json()
            author = data['author']
            body = data['body']
            if isinstance(body, str) and not body.isspace() and len(author) > 0:
                database_connection.create_question(body,author)
                return Response(json.dumps(['Question added successfully']), status=201, mimetype='application/json')
            return Response(json.dumps(['All fields should not be empty']), status=404, mimetype='application/json')


api.add_resource(QuestionsBox, '/questions')


class Question(Resource):
    def get(self, questionId):
        question_dict = database_connection.get_specific_question(questionId)
        if question_dict:
           return make_response(jsonify(question_dict), 200)

        return Response(json.dumps(['Question does not exist']), status=404, mimetype='application/json')

    def delete(self, questionId):
        database_connection.delete_questions(questionId)
        return {'message': 'Question {} deleted'.format(questionId)}, 204


api.add_resource(Question, '/questions/<int:questionId>')


class AddAnswer(Resource):
    def post(self, questionId):
        data = request.get_json()
        body = data['body']
        author = data['author']
        if isinstance(body, str) and not body.isspace() and len(body) > 0:
            database_connection.answer_question(body,author,questionId), 201
            return Response(json.dumps(['Answer added successfully']), status=201, mimetype='application/json')
        return Response(json.dumps(['All fields must not be empty']), status=404, mimetype='application/json')


api.add_resource(AddAnswer, '/questions/<int:questionId>/answers')


class RegisterAPI(Resource):
    def post(self):
        if not request.is_json:
            return Response(json.dumps(['JSON is missing']), status=400, mimetype='application/json')
        data = request.get_json()
        email = data['email']
        username = data['username']
        password = data['password']
        confirm_password = data['confirm_password']
        if not validators.email('solomonbwire@gmail.com'):
            return Response(json.dumps(['Please provide a valid email address!']), status=400, mimetype='application/json')
        elif not username:
            return Response(json.dumps(['User name is required!']), status=400, mimetype='application/json')
        elif not password:
            return Response(json.dumps(['please provide your password!']), status=400, mimetype='application/json')
        elif not confirm_password:
            return Response(json.dumps(['please confirm your password!']), status=400, mimetype='application/json')
        if isinstance(username,str) and not username.isspace() and len(username) > 1:
            if confirm_password == password:
                database_connection.register(email,username,password)
                return {'message': 'User registered successfully'}, 201
            return Response(json.dumps(['password not matching!']), status=400, mimetype='application/json')
        return Response(json.dumps(['Please provide a valid input!']), status=400, mimetype='application/json')


api.add_resource(RegisterAPI, '/auth/register')


class Login(Resource):
    def post(self):
        data = request.get_json()
        if not data:
            return Response(json.dumps(['Invalid format, JSON is missing!']), status=400, mimetype='application/json')

        username = data['username']
        password = data['password']

        if not username:
            return Response(json.dumps(['username is required!']), status=400, mimetype='application/json')
        elif not password:
            return Response(json.dumps(['Password can not be empty!']), status=400, mimetype='application/json')
        users = database_connection.get_user(username)
        print(users)
        user = [user for user in users if user[1] == username and check_password_hash(user[2],str(password))]
        if not user:
            return Response(json.dumps(['Invalid username or password!']), status=400, mimetype='application/json')
        access_token = create_access_token(identity=username, fresh=timedelta(minutes=60))
        return make_response(jsonify(access_token=access_token), 200)


api.add_resource(Login, '/auth/login')
