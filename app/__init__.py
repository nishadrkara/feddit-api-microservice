from flask import Flask
from flask_restx import Api


def create_app(config_class='config.Config'):
    app = Flask(__name__)
    app.config.from_object(config_class)
    api = Api(app, version='1.0', title='My API',
              description='A simple demonstration of a Flask REST API with Swagger')
    from app.routes import initialize_routes
    initialize_routes(api)

    return app
