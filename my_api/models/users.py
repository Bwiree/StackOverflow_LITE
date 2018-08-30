from werkzeug.security import generate_password_hash

class User:
    def __init__(self,email, username, password):
        self.email = email
        self.username = username
        self.password = password