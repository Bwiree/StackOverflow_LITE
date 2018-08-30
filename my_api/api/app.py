from flask import Flask
from my_api.instance.config import DevelopmentConfig
from flask_jwt_extended import JWTManager

app = Flask(__name__, instance_relative_config=True)

app.config.from_object(DevelopmentConfig)
app.config['RESTPLUS_VALIDATE'] = True
app.config['JWT_SECRET_KEY'] = 'random#$8990000000secret'


jwt = JWTManager(app)
