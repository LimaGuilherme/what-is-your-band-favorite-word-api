import os

from flask import Flask

from app import api, config as config_module

config = config_module.get_config()

web_app = Flask(__name__)
web_app.config.from_object(config)

api.create_api(web_app)


@web_app.after_request
def add_cache_header(response):
    response.headers['Cache-Control'] = "no-cache, no-store, must-revalidate"
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response


def run():
    web_app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 6669)), debug=True)
