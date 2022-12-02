from flask import Flask, request

from controllers.auth_controller import valid_token
from controllers.registration.database_controller import *


def init_app(app: Flask):
    @app.route("/DatabaseRegistration", methods=["POST"])
    def database_register():
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]
            token_decode = valid_token(token)
            try:
                client = request.json["client"]
                charset = request.json["charset"]
                server = request.json["server"]
                structure = request.json["structure"]
                instance = request.json["instance"]
                db_user = request.json["dbUser"]
                brands = request.json["brands"]
                size = request.json["size"]
                dta_dmpbak = request.json["dtaDmpBak"]
                result = registration_database(client,
                                               charset,
                                               server,
                                               structure,
                                               instance,
                                               db_user,
                                               brands,
                                               size,
                                               dta_dmpbak,
                                               token_decode["tipo"])
                return result
            except TypeError:
                return {"message": "Ocorreu um erro ao cadastrar o banco!"}, 500
        else:
            return {"message": "Token de autenticação inválido."}, 401

    @app.route("/DatabaseEdit", methods=["PUT"])
    def database_edit():
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]
            token_decode = valid_token(token)
            try:
                db_id = request.json["dbID"]
                client = request.json["client"]
                charset = request.json["charset"]
                server = request.json["server"]
                structure = request.json["structure"]
                instance = request.json["instance"]
                db_user = request.json["dbUser"]
                brands = request.json["brands"]
                size = request.json["size"]
                dta_dmpbak = request.json["dtaDmpBak"]
                result = edit_database(db_id,
                                       client,
                                       charset,
                                       server,
                                       structure,
                                       instance,
                                       db_user,
                                       brands,
                                       size,
                                       dta_dmpbak,
                                       token_decode["tipo"])
                return result
            except TypeError:
                return {"message": "Ocorreu um erro ao alterar o banco!"}, 500
        else:
            return {"message": "Token de autenticação inválido."}, 401

    @app.route("/DatabaseDelete", methods=["DELETE"])
    def database_delete():
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]
            token_decode = valid_token(token)
            try:
                db_id = request.headers["dbID"]
                result = delete_database(db_id, token_decode["tipo"])
                return result
            except TypeError:
                return {"message": "Ocorreu um erro ao listar os bancos!"}, 500
        else:
            return {"message": "Token de autenticação inválido."}, 401

    @app.route("/DatabaseList", methods=["GET"])
    def database_list():
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]
            token_decode = valid_token(token)
            try:
                result = list_database(token_decode["tipo"])
                return result
            except TypeError:
                return {"message": "Ocorreu um erro ao listar os bancos!"}, 500
        else:
            return {"message": "Token de autenticação inválido."}, 401
