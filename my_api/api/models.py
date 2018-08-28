import uuid

from flask import jsonify

answers = []


class User:
    def __init__(self, email, username, password):
        self.id = uuid.uuid4().int
        self.email = email
        self.username = username
        self.password = password


class Questions(object):
    def __init__(self, question, author, create_date, answers):
        self.questionId = uuid.uuid4().int
        self.question = question
        self.author = author
        self.create_date = create_date
        self.answers = answers

    def get_all_questions(self):
        questions = [
            {
                'questionId': self.questionId,
                'question': self.question,
                'author': self.author,
                'create_date': self.create_date,
                'answer': self.answer
            }
        ]
        return jsonify({'questions': questions})