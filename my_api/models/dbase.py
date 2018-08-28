import psycopg2

class DatabaseConnection:
    def __init__(self):
        try:
            self.connection = psycopg2.connect(

            )
        except:
            print("Could not connect to server")