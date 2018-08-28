from flask import Flask

from my_api.api.app import blue_print
from my_api.instance.config import DevelopmentConfig


def create_app(config):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(DevelopmentConfig)
    app.register_blueprint(blue_print)

    return app
