"""Boot file"""
from flask import Flask
from extensions import database, bcrypt, email, cors

from routes import auth_routes
from routes import dashboard_routes
from routes.registration import user_routes
from routes.registration import teams_routes
from routes.registration import database_routes
from routes.registration import occurrences_routes
from routes.requests import request_routes
from routes.requests import error_request_routes
from routes.requests import alteration_request_routes
from routes.requests import customization_request_routes



def register_extensions(app):
    bcrypt.init_app(app)
    database.init_app(app)
    email.init_app(app)

    cors.init_app(app)


def create_app():
    app = Flask(__name__)

    register_extensions(app)

    auth_routes.init_app(app)
    dashboard_routes.init_app(app)

    user_routes.init_app(app)
    teams_routes.init_app(app)
    database_routes.init_app(app)
    occurrences_routes.init_app(app)

    request_routes.init_app(app)
    
    error_request_routes.init_app(app)
    alteration_request_routes.init_app(app)
    customization_request_routes.init_app(app)

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)
