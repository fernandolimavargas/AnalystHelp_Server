from flask import Flask, request

from controllers.auth_controller import auth_login, password_recovery_email, send_email_recovery, send_email_access


def init_app(app: Flask):
    @app.route('/Login', methods=["POST"])
    def login():
        user = request.json['user']
        password = request.json['password']
        acess_token = auth_login(user, password)

        return acess_token

    @app.route('/PasswordRecovery', methods=["GET", "POST"])
    def password_recovery():
        if request.method == "GET":
            email = request.args.get('email')
            result = password_recovery_email(email)

            return result

        email = request.json['email']

        result = send_email_recovery(email)

        return result

    @app.route('/RequestAccess', methods=["POST"])
    def requests_access():
        email = request.json['email']

        result = send_email_access(email)

        return result
