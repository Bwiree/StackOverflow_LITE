from flask import Blueprint, request, Response, jsonify, make_response
from flask_restful import Resource,Api
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from my_api.models.dbase import DatabaseConnection
import json

auth_blueprint = Blueprint('auth', __name__, url_prefix='/api/v1')
api = Api(auth_blueprint)

database_connection = DatabaseConnection()


class QuestionsBox(Resource):
    def get(self):
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
        questionId = data['questionId']
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
        if not email:
            return Response(json.dumps(['email address is missing!']), status=400, mimetype='application/json')
        elif not username:
            return Response(json.dumps(['User name is required!']), status=400, mimetype='application/json')
        elif not password:
            return Response(json.dumps(['please provide your password!']), status=400, mimetype='application/json')
        elif not confirm_password:
            return Response(json.dumps(['please confirm your password!']), status=400, mimetype='application/json')
        if isinstance(email,str) and not username.isspace() and len(username) > 1:
            if confirm_password == password:
                database_connection.register(email,username,password)
                return {'message': 'User registered successfully'}, 201
            return Response(json.dumps(['password not matching!']), status=400, mimetype='application/json')
        return Response(json.dumps(['Please provide a valid input!']), status=400, mimetype='application/json')


api.add_resource(RegisterAPI, '/auth/register')


class Login(Resource):
    def post(self):
        data = request.get_json()
        username = data['username']
        password = data['password']
        user, password_hash = database_connection.get_user(username)
        if user and database_connection.confirm_password_hash(password, password_hash):
            print('The user is confirmed')
            access_token = create_access_token(identity=username)
            return {'message': 'Token created',
                    'access_token': access_token}, 201
        return {'message': 'Invalid username or password'}, 400


api.add_resource(Login, '/auth/Login')
