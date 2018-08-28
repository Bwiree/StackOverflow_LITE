from flask import jsonify

answers = []


class Questions(object):
    def __init__(self, questionId, question, author, create_date, answers):
        self.questionId = questionId
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