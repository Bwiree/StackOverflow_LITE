import json
from my_api.tests.testbase import TestBase

BASE_URL = 'http://127.0.0.1:5000/api/v1'


class UserTest(TestBase):
    def test_user_register(self):
        with self.client as client:
            response = client.post(BASE_URL + '/auth/register', json=dict(self.register))
            self.assertEqual(response.status_code, 201)

    def test_user_login(self):
        with self.client as client:
            client.post(BASE_URL + '/auth/register', json=dict(self.register))
            response = client.post(BASE_URL + '/auth/login', json=dict(self.login))
            self.assertEqual(response.status_code, 400)


class QuestionTest(TestBase):
    def test_post_question(self):
        with self.client as client:
            client.post(BASE_URL + '/auth/login', json=dict(self.login))
            response = client.post(BASE_URL + '/auth/login', json=dict(self.login))
            response_data = json.loads(response.data.decode())
            test_response = client.post(BASE_URL + '/questions',
                                        headers={'Authorization': 'Bearer ' + response_data['access_token']}, \
                                        json=dict(self.question_add))
            self.assertEqual(test_response.status_code, 201)

    def test_get_questions(self):
        with self.client as client:
            client.post(BASE_URL + '/auth/signup', json=dict(self.signup))
            login_response = client.post(BASE_URL + '/auth/login', json=dict(self.login))
            login_data = json.loads(login_response.data.decode())
            client.post(BASE_URL + '/questions', headers={'Authorization': 'Bearer ' + login_data['access_token']}, \
                        json=dict(self.question_add))

            response = client.get(BASE_URL + '/questions')
            self.assertEqual(response.status_code, 200)

    def test_get_specific_question(self):
        with self.client as client:
            client.post(BASE_URL + '/questions', json=dict(self.question))
            login_response = client.post(BASE_URL + '/auth/login', json=dict(self.login))
            login_data = json.loads(login_response.data.decode())
            client.post(BASE_URL + '/questions', headers={'Authorization': 'Bearer ' + login_data['access_token']}, json=dict(self.question_add))
            client.post(BASE_URL + '/questions', headers={'Authorization': 'Bearer ' + login_data['access_token']}, json=dict(self.another_question))

            response = client.get(BASE_URL + '/questions/2')
            self.assertEqual(response.status_code, 200)

    def test_delete_question(self):
        with self.client as client:
            client.post(BASE_URL + '/auth/signup', json=dict(self.register))
            login_response = client.post(BASE_URL + '/auth/login', json=dict(self.login))
            login_data = json.loads(login_response.data.decode())
            client.post(BASE_URL + '/questions', headers={'Authorization': 'Bearer ' + login_data['access_token']}, json=dict(self.question_add))
            client.post(BASE_URL + '/questions', headers={'Authorization': 'Bearer ' + login_data['access_token']}, json=dict(self.another_question))
            client.get(BASE_URL + '/questions/2')
            response = client.delete(BASE_URL + '/questions/2',
                                     headers={'Authorization': 'Bearer ' + login_data['access_token']})
            self.assertEqual(response.status_code, 204)


class AnswerTest(TestBase):
    def test_post_answer_to_question(self):
        with self.client as client:
            client.post(BASE_URL + '/auth/register', json=dict(self.register))
            login_response = client.post(BASE_URL + '/auth/login', json=dict(self.login))
            login_data = json.loads(login_response.data.decode())
            print(login_response.data)
            print('lg', login_data)
            client.post(BASE_URL + '/questions', headers={'Authorization': 'Bearer ' + login_data['access_token']}, json=dict(self.question_add))
            client.post(BASE_URL + '/questions', headers={'Authorization': 'Bearer ' + login_data['access_token']}, json=dict(self.another_question))
            client.get(BASE_URL + '/questions/1')
            response = client.post(BASE_URL + '/questions/1/answers', json=dict(self.answer_post))
            response.headers["Authorization"] = 'Bearer ' + login_data['access_token']
            self.assertEqual(response.status_code, 201)

    def test_existing_answer(self):
        with self.client as client:
            client.post(BASE_URL + '/auth/register', json=dict(self.register))
            login_response = client.post(BASE_URL + '/auth/login', json=dict(self.login))
            login_data = json.loads(login_response.data.decode())
            client.post(BASE_URL + '/questions', headers={'Authorization': 'Bearer ' + login_data['access_token']}, json=dict(self.question_add))
            client.post(BASE_URL + '/questions', headers={'Authorization': 'Bearer ' + login_data['access_token']}, json=dict(self.another_question))
            client.get(BASE_URL + '/questions/1')
            client.post(BASE_URL + '/questions/1/answers',
                        headers={'Authorization': 'Bearer ' + login_data['access_token']}, json=dict(self.answer_post))
            response = client.post(BASE_URL + '/questions/1/answers',
                                   headers={'Authorization': 'Bearer ' + login_data['access_token']}, json=dict(self.answer_post))
            self.assertEqual(response.status_code, 406)

    def test_empty_answer_posted(self):
        with self.client as client:
            login_response = client.post(BASE_URL + '/auth/login', json=dict(self.login))
            login_data = json.loads(login_response.data.decode())
            client.post(BASE_URL + '/questions', headers={'Authorization': 'Bearer ' + login_data['access_token']}, \
                        json=dict(self.question_add))
            client.post(BASE_URL + '/questions', headers={'Authorization': 'Bearer ' + login_data['access_token']}, \
                        json=dict(self.another_question))
            client.get(BASE_URL + '/questions/1')
            response = client.post(BASE_URL + '/questions/1/answers',
                                   headers={'Authorization': 'Bearer ' + login_data['access_token']},json=dict(self.answer_post_empty))
            self.assertEqual(response.status_code, 406)