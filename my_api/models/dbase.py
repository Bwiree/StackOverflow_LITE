import psycopg2


class DatabaseConnection:
    def __init__(self):
        try:
            self.connection = psycopg2.connect(
                "dbname='stackoverflow' user='postgres' host='localhost' password='boy' port='5432'")
            self.connection.autocommit = True
            self.cursor = self.connection.cursor()

        except:
            print("Could not connect to server")

    def create_users_table(self):
        create_table_command = """CREATE TABLE IF NOT EXISTS users(
        id SERIAL PRIMARY KEY,  
        email VARCHAR(100) NOT NULL, 
        username VARCHAR(30),
        password VARCHAR(100) NOT NULL
        )"""
        self.cursor.execute(create_table_command)

    def insert_record(self, tablename, ):
        record = ("Juma", "saffgdd@gmail.com", "jsohjhhrn")
        insert_command = "INSERT INTO users(email, username, password) VALUES('" + record[0] + "','" + record[1] + "','" + record[2] + "');"
        print(insert_command)
        self.cursor.execute(insert_command)

    def create_questions_table(self):
        create_table_command = """CREATE TABLE IF NOT EXISTS questions(
        questionId SERIAL PRIMARY KEY, 
        question VARCHAR(150), 
        author VARCHAR(50), 
        create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );"""
        self.cursor.execute(create_table_command)

    def create_answers_table(self):
        create_table_command = """CREATE TABLE IF NOT EXISTS answers(
        questionId serial PRIMARY KEY, 
        author VARCHAR(50), 
        answer VARCHAR(150) 
        );"""
        self.cursor.execute(create_table_command)


if __name__ == '__main__':
    connect = DatabaseConnection()
    connect.create_users_table()
    connect.create_questions_table()
    connect.create_answers_table()
    connect.insert_record()
