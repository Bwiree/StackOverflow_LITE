import datetime

from flask import request, jsonify, make_response, Blueprint
from flask_restful import Resource, Api

blue_print = Blueprint('qns_bp', __name__, url_prefix='/api/v1')

api = Api(blue_print)
questions = []


class QuestionsBox(Resource):
    def get(self):
        if len(questions) == 0:
            return jsonify({'message': 'No question posted'})
        return jsonify({'questions': questions})

    def post(self):
        request_data = request.get_json()
        questionId = len(questions) + 1
        qn = {
            'questionId': questionId,
            'question': request_data['question'],
            'author': request_data['author'],
            'create_date': datetime.datetime.now().strftime('%A, %d. %B %Y %I:%M%p'),
            'answer': []
              }
        if isinstance(request_data['question'], str) and not request_data['question'].isspace() and len(request_data['question'])>0:
            questions.append(qn)
            return make_response(jsonify({'message':'Question Added'}), 201)
        return make_response(jsonify({'message': 'Invalid Question input'}), 422)


api.add_resource(QuestionsBox, '/questions')


class GetQuestion(Resource):
    def get(self,questionId):
        for question in questions:
            if question['questionId'] == questionId:
                return jsonify(question)
        return make_response(jsonify({'message':'question could not be found'}), 404)


api.add_resource(GetQuestion, '/questions/<int:questionId>')


class AddAnswer(Resource):
    def post(self,questionId):
        request_data = request.get_json()
        for question in questions:
            if question['questionId'] == questionId:
                answer = request_data['answers']
                if isinstance(request_data['answers'], str) and not answer.isspace() and len(answer)>0:
                    question['answers'].append(answer)
                    return make_response(jsonify({'message':'Answer has been addded'}), 201)
                return make_response(jsonify({'message':'Invalid answer'}), 422)
        return make_response(jsonify({'message':'question not found'}), 404)


api.add_resource(AddAnswer, '/questions/<int:questionId>/answers')
