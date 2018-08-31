import unittest
from my_api.instance.config import TestingConfig
from my_api.api import create_app
from my_api.models.dbase import DatabaseConnection


class TestBase(unittest.TestCase):

    def setUp(self):
        self.app = create_app(TestingConfig)
        self.client = self.app.test_client()
        db = DatabaseConnection()
        db.create_users_table()
        db.create_questions_table()
        db.create_answers_table()

        self.user = {
            "id": "1",
            "email": "solomonbwire@gmail.com",
            "username": "Bwire",
            "password": "1234"
        }
        self.question = {
            "qestionId": "1",
            "userId": "1",
            "body": "What is programming?",
            "author": "Bwire",
            "create_date": ""
        }
        self.answer = {
            "answerId": "1",
            "questionId": "Set of rules",
            "body": "1",
            "author": "Sharon",
            "accept_status": "t",
            "published_date": ""
        }
        self.register = {
            "email": "sdyftybhv@gmail.com",
            "username": "Ben",
            "password": "12345678",
            "confirm_password": "12345678"
        }
        self.login = {
            "username": "sharon",
            "password": "1234"
        }

        self.question_add = {
            "question": "What is c++?"
        }
        self.another_question = {
            "question": "What is python?"
        }
        self.answer_post = {
            "answer": "hell nooo"
        }
        self.answer_post_empty = {
            "answer": ""
        }

    def tearDown(self):
        db = DatabaseConnection()
        db.drop_table()