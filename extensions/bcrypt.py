from flask_bcrypt import Bcrypt


def init_app(app):
    Bcrypt(app)


bcrypt = Bcrypt()
