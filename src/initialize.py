from flask import Flask

from src import api, configurations as config_module

config = config_module.get_config()

web_app = Flask(__name__)
web_app.config.from_object(config)

api.create_api(web_app)
