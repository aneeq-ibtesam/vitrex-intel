from flask import Flask
from config import config
from .extensions import mongo

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    mongo.init_app(app)

    from .web import web as web_blueprint
    app.register_blueprint(web_blueprint)

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    return app
