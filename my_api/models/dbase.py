import psycopg2
from pprint import pprint
from passlib.hash import pbkdf2_sha256 as sha256
from my_api.models.questions import Question
from my_api.models.users import User
from my_api.models.answers import Answer


class DatabaseConnection(object):
    def __init__(self):
        try:
            self.connection = psycopg2.connect(
                "dbname='stackoverflow' "
                "user='postgres' "
                "host='localhost'"
                " password='boy' "
                "port='5432'"
            )
            self.connection.autocommit = True
            self.cursor = self.connection.cursor()
            self.queries = []

        except (Exception, psycopg2.DatabaseError) as e:
            pprint(e, "Could not connect to server")

    def create_users_table(self):
        try:
            create_table_command = """CREATE TABLE IF NOT EXISTS users(
            id SERIAL PRIMARY KEY,  
            email VARCHAR(100) NOT NULL, 
            username VARCHAR(30),
            password VARCHAR(100) NOT NULL
            )"""
            self.cursor.execute(create_table_command)

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def create_questions_table(self):
        try:
            create_table_command = """CREATE TABLE IF NOT EXISTS questions(
            questionId SERIAL PRIMARY KEY, 
            userId int,
            body VARCHAR(500), 
            author VARCHAR(50), 
            create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (userId) REFERENCES users(id) ON DELETE CASCADE
            );"""
            self.cursor.execute(create_table_command)

        except(Exception, psycopg2.DatabaseError) as error:
            print(error)

    def create_answers_table(self):
        try:
            create_table_command = """CREATE TABLE IF NOT EXISTS answers(
            answerId serial PRIMARY KEY,
            questionId INT,
            body VARCHAR(150),
            author VARCHAR(50),
            accept_status boolean DEFAULT FALSE,
            published_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );"""
            self.cursor.execute(create_table_command)

        except(Exception, psycopg2.DatabaseError) as error:
            print(error)

    def drop_table(self, *table_names):
        for table_name in table_names:
            drop_table = "DROP TABLE IF EXISTS {} CASCADE".format(table_name)
            pprint("Tables dropped")
            self.cursor.execute(drop_table)

    def register(self,email, username, password):
        password = self.hash_password(password)
        user = User(email, username, password)
        insert_command = "INSERT INTO users(email, username, password) VALUES('{}' ,'{}','{}')".format(user.email, user.username, user.password)
        pprint(insert_command)
        self.cursor.execute(insert_command)

    def get_user(self, username):
        try:

            sql_command = "SELECT *FROM users WHERE username = '{}'".format(username)
            self.cursor.execute(sql_command)
            user = self.cursor.fetchone()
            email = user[1]
            username = user[2]
            password = user[3]
            return email, username, password
        except Exception as e:
            # print({'error': 'User not found {}'.format(e)})
            return {'error': 'User not found {}'.format(e)}

    def create_question(self, body, author):
        user_sql = "SELECT id FROM users WHERE username = '{}'".format('Bwire')
        self.cursor.execute(user_sql)
        user = self.cursor.fetchone()

        questions = Question(body,author)
        sql_command = "INSERT INTO questions(userId, body,author) VALUES ('{}','{}','{}')".format(user[0], questions.body, questions.author)
        pprint(sql_command)
        self.cursor.execute(sql_command)

    def query_all_questions(self):
        queries = []
        try:
            sql_command = "SELECT *FROM questions"
            self.cursor.excute(sql_command)
            items = self.cursor.fetchall()
            if items:
                for item in items:
                    queries.append(item)
                return queries
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        else:
            return queries

    def get_all_questions(self):
        sql = "SELECT *FROM questions"
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        questions = [questions for questions in rows]
        return {'all_questions': questions}

    def get_all_answers(self):
        self.cursor.execute("SELECT * FROM answers")
        answers = self.cursor.fetchall()
        return answers

    def get_specific_question(self, questionId):
        try:
            question_sql = "SELECT *FROM questions WHERE questionId = %s "
            self.cursor.execute(question_sql, (questionId,))
            question = self.cursor.fetchone()
            print(question)
            answers_sql = "SELECT * FROM answers WHERE questionId = %s "
            self.cursor.execute(answers_sql, (questionId,))
            answers = self.cursor.fetchall()
            answersList = [row for row in answers]

            return {'question': {'author': question[3],
                                 'body': question[2],
                                 'answers': answersList
                                 }}
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def answer_question(self, questionId, body, author):
        answers = Answer(questionId, body, author)
        sql = "INSERT INTO answers(questionId, body, author) VALUES (%s, %s, %s);"
        print(sql)
        self.cursor.execute(sql, (answers.questionId, str(answers.body), answers.author))

    def hash_password(self, password):
        return sha256.hash(password)

    def confirm_password_hash(self, password, password_hash):
        return sha256.verify(password, password_hash)

    def delete_questions(self, questionId):
        sql = "DELETE FROM questions WHERE  questionId = {} ".format(
            questionId)
        rows_deleted = self.cursor.rowcount
        print(rows_deleted)
        self.cursor.execute(sql)
        return {"message": "Question {} deleted".format(questionId)}

    def update(self, accept_status, answerId):
        sql = 'UPDATE answers SET accept_status = {} WHERE answerId = {}'.format(accept_status, answerId)
        self.cursor.execute(sql)
        return {'message': 'Answer status updated'}


if __name__ == '__main__':
    connect = DatabaseConnection()
    connect.create_users_table()
    connect.create_questions_table()
    connect.create_answers_table()
    connect.register(email="solomonbwire@gmail.com",username="Bwire",password="nodsbsbn" )
    connect.create_question(body="What is programming",author="Jackie")
    connect.get_all_questions()
    # connect.delete_questions(questionId=1)
