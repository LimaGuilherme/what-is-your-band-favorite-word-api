import os

from flask import Flask

from src import api, configurations as config_module

config = config_module.get_config()

web_app = Flask(__name__)
web_app.config.from_object(config)

api.create_api(web_app)


def run():
    web_app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 6669)), debug=True)
