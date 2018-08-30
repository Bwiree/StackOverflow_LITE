from my_api.instance import config
from my_api.api import create_app


app = create_app(config.DevelopmentConfig)

if __name__ == '__main__':
    app.run()