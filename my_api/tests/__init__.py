from my_api.api import app
from my_api.instance.config import Config

app.config.from_object(Config)