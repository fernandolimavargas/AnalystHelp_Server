import jwt
from flask import render_template
from flask_mail import Message
from extensions.email import mail

from models.models import GESTOR, HELPER, ANALISTA
from extensions.bcrypt import bcrypt
from extensions.database import database
from random import choice
import string


def auth_login(user, password, remember):
    user = user + '@linx.com.br'
    usuario = GESTOR.query.filter_by(EMAIL=user).first() or HELPER.query.filter_by(
        EMAIL=user).first() or ANALISTA.query.filter_by(EMAIL=user).first()


    if usuario and bcrypt.check_password_hash(usuario.SENHA, password):
        payload = {
            "id": usuario.id,
            "email": usuario.EMAIL,
            "tipo": usuario.TIPO
        }

        token = jwt.encode(payload, 'secret', algorithm="HS256")

        result = {"id": usuario.id, "name": usuario.USUARIO, "email": usuario.EMAIL,
                  "tipo": usuario.TIPO, "token": token}

        return result
    else:
        return {"message": "Usuário e/ou senha não encontrados!"}, 401


def valid_token(token=None):
    try:
        token = jwt.decode(token, 'secret', algorithms=["HS256"])

        return token
    except:
        return {"message": "Token de autenticação invalido."}, 401


def send_email_recovery(email):
    usuario = (GESTOR.query.filter_by(EMAIL=email).first()
               or HELPER.query.filter_by(EMAIL=email).first()
               or ANALISTA.query.filter_by(EMAIL=email).first())

    if usuario:
        msg = Message('Recuperação de senha',
                      sender='joao.marconi@linx.com.br', recipients=[email])
        msg.html = render_template(
            'resetpasswordmail.html', email=usuario.EMAIL)
        mail.send(msg)
        return {"message": "E-mail de recuperação enviado com sucesso!"}, 200

    return {"message": "E-mail não encontrado, favor solicitar acesso!"}, 401


def password_recovery_email(email):
    usuario = (GESTOR.query.filter_by(EMAIL=email).first()
               or HELPER.query.filter_by(EMAIL=email).first()
               or ANALISTA.query.filter_by(EMAIL=email).first())

    if usuario:
        tamanho = 12
        valores = string.ascii_lowercase + string.digits
        password = ''

        for i in range(tamanho):
            password += choice(valores)

        usuario.SENHA = bcrypt.generate_password_hash(password)

        database.session.commit()

        msg = Message('Recuperação de senha',
                      sender='joao.marconi@linx.com.br', recipients=[email])
        msg.html = render_template(
            'resetpasswordmail2.html', novasenha=password)
        mail.send(msg)

        return {"message": "Sua nova senha foi enviada para o seu e-mail!"}, 200

    return {"message": "Erro, favor comunicar o administrador do sistema!"}, 500


def send_email_access(email):
    usuario = (GESTOR.query.filter_by(EMAIL=email).first()
               or HELPER.query.filter_by(EMAIL=email).first()
               or ANALISTA.query.filter_by(EMAIL=email).first())

    if usuario:
        return {"message": "O e-mail informado ja tem acesso, solicite o reset de senha!"}, 401
    
    if email.split('@')[1] != 'linx.com.br':
        return {"message": "O e-mail informado não pertente a linx!"}, 401

    nome = email.split('@')[0].replace('.', ' ').title()

    msg = Message('Solicitação de acesso', sender='joao.marconi@linx.com.br',
                  recipients=['joao.marconi@linx.com.br'])
    msg.html = render_template('requestaccess.html', nome=nome, email=email)
    mail.send(msg)

    return {"message": "Solicitação enviada com sucesso!"}, 200
