from flask import Flask
from flask_mail import Mail


def init_app(app: Flask):
    app.config['MAIL_SERVER'] = 'smtp-mail.outlook.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USERNAME'] = 'joao.marconi@linx.com.br'
    app.config['MAIL_PASSWORD'] = 'asdfqwer123456789*'
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False

    Mail(app)


mail = Mail()
