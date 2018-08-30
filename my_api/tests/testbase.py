import unittest
from my_api.api import create_app
from flask import current_app

from my_api.api import app
from my_api.models.questions import Question
from my_api.models.answers import Answer
from my_api.auth import views
from my_api.instance.config import Config
from my_api.models.dbase import DatabaseConnection
from my_api.instance.config import TestingConfig


class TestBase(unittest.TestCase):
    def creating_app(self):
        app = create_app()
        app.config.from_object(TestingConfig)
        return app

    def setUp(self):
        self.app = self.creating_app()
        self.connection = DatabaseConnection()
        self.connection.create_users_table()
        self.connection.create_questions_table()
        self.connection.create_answers_table()

        self.connection.register(email="solomonbwire@gmail.com",username="Bwire",password="12345678")

    def tearDown(self):
        self.connection.drop_table('users')
        self.connection.drop_table('questions')
        self.connection.drop_table('answers')


def createQnsList():
    '''Generates a List of five questions with different topics
    and links answers to them'''

    QnsList = []
    body = ""

    authors = [0, '', '', '', '', '']

    for i in range(1, 6):
        Qn = Question(authors[i], body)
        QnsList.append(Qn.__repr__())
    return QnsList


questionsList = createQnsList()


def createAnsList():
    '''Generates list of five answers'''
    AnsList = []
    body = ""

    l = [question['questionId'] for question in questionsList]
    qnIds = [id for id in l]
    qnIds[:0] = [0]

    for i in range(1, 6):
        Ans = Answer(body, qnIds[i])
        AnsList.append(Ans.__repr__())
    return AnsList


answersList = createAnsList()