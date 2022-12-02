from flask import Flask, request

from controllers.auth_controller import valid_token
from controllers.requests.request_controller import *

def init_app(app: Flask):
    @app.route("/ReqMovements", methods=["GET"])
    def req_movements_list():
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]
            token_decode = valid_token(token)
            try:
                request_id = request.headers["requestId"]
                result = request_movements_list(token_decode["id"], token_decode["tipo"], request_id)
                return result
            except TypeError:
                return {"message": "Ocorreu um erro ao listar as movimentações!"}, 500
        else:
            return {"message": "Token de autenticação inválido."}, 401

    @app.route('/TestConnection', methods=["POST"])
    def test_con():
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]
            valid_token(token)
            try:
                structure = request.json["structure"]
                server = request.json["server"]
                database = request.json["database"]
                username = request.json["username"]
                password = request.json["password"]
                result = test_connection(structure, server, database, username, password)
                return result
            except TypeError:
                return {"message": "Ocorreu um erro ao validar conexão com o banco!"}, 500
        else:
            return {"message": "Token de autenticação inválido."}, 401

    @app.route('/SearchMenu', methods=["GET"])
    def srch_menu():
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]
            valid_token(token)
            try:
                cod_menu = request.headers["codMenu"]
                result = search_menu(cod_menu)
                return result
            except ValueError as e:
                return {"message": "Ocorreu um erro ao buscar o menu"}, 500
        else:
            return {"message":"Token de autenticação inválido."}, 401
        