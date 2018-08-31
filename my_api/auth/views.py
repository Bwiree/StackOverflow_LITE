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
        question_dict = database_connection.get_all_questions()
        if current_user:
            if question_dict:
                return make_response(jsonify(question_dict), 200)
            return Response(json.dumps(['No questions to display!']), status=404, mimetype='application/json')
        return Response(json.dumps(['You have no access permission!']), status=401, mimetype='application/json')

    @jwt_required
    def post(self):
        current_user = get_jwt_identity()
        data = request.get_json()
        author = data['author']
        body = data['body']
        if current_user:

            if isinstance(body, str) and not body.isspace() and len(author) > 0:
                database_connection.create_question(body,author)
                return Response(json.dumps(['Question added successfully']), status=201, mimetype='application/json')
            return Response(json.dumps(['All fields should not be empty']), status=404, mimetype='application/json')


api.add_resource(QuestionsBox, '/questions')


class Question(Resource):
    @jwt_required
    def get(self, questionId):
        current_user = get_jwt_identity()
        if current_user:
            question_dict = database_connection.get_specific_question(questionId)
            if question_dict:
                return make_response(jsonify(question_dict), 200)
            return Response(json.dumps(['Question does not exist']), status=404, mimetype='application/json')

    @jwt_required
    def delete(self, questionId):
        current_user = get_jwt_identity()
        if current_user:
            database_connection.delete_questions(questionId)
            return {'message': 'Question {} deleted'.format(questionId)}, 204
        return Response(json.dumps(['You do not have access permission!']), status=404, mimetype='application/json')


api.add_resource(Question, '/questions/<int:questionId>')


class AddAnswer(Resource):
    @jwt_required
    def post(self, questionId):
        current_user = get_jwt_identity()
        data = request.get_json()
        body = data['body']
        author = data['author']
        if current_user:
            if isinstance(body, str) and not body.isspace() and len(body) > 0:
                database_connection.answer_question(body,author,questionId), 201
                return Response(json.dumps(['Answer added successfully']), status=201, mimetype='application/json')
            return Response(json.dumps(['All fields must not be empty']), status=404, mimetype='application/json')
        return Response(json.dumps(['You do not have access permission']), status=404, mimetype='application/json')


api.add_resource(AddAnswer, '/questions/<int:questionId>/answers')


# class AnswerUpdate(Resource):
#     def put(self, answerId):
#         data = request.get_json
#         answerId = answerId
#         print(answerId)
#         accept_status = data['accept_status']
#         database_connection.update(accept_status, answerId)
#         return {'message': 'Answer status updated'}, 201


# api.add_resource(AnswerUpdate, '/questions/<int:questionId>/answers/<int:answerId>')


class RegisterAPI(Resource):
    def post(self):
        data = request.get_json()
        if not data:
            return Response(json.dumps(['JSON is missing']), status=400, mimetype='application/json')
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
        user = [user for user in users if user[2] == username and check_password_hash(user[3],str(password))]
        if not user:
            return Response(json.dumps(['Invalid username or password!']), status=400, mimetype='application/json')
        access_token = create_access_token(identity=username, fresh=timedelta(minutes=6000))
        return make_response(jsonify(access_token=access_token), 200)


api.add_resource(Login, '/auth/login')
