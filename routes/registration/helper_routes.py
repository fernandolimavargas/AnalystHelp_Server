from multiprocessing.sharedctypes import Value
from flask import Flask, request

from controllers.auth_controller import valid_token
from controllers.registration.helper_controller import *

def init_app(app: Flask):
    @app.route("/HelperRegistration", methods=["POST"])
    def helper_register():
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]
            token_decode = valid_token(token)
            try:
                name = request.json["name"]
                email = request.json["email"]
                password = request.json["password"]
                result = registration_helper(name, email, password, token_decode["tipo"])
                return result
            except TypeError:
                return {"message": "Ocorreu um erro ao cadastrar o helper!"}, 500
        else: 
            return {"message": "Token de autenticação inválido."}, 401

    @app.route("/HelperEdit", methods=["PUT"])
    def helper_edit():
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]
            token_decode = valid_token(token)
            try:
                helper_id = request.json["helperID"]
                name = request.json["name"]
                email = request.json["email"]
                password = request.json["password"]
                result = edit_helper(helper_id, name, email, password, token_decode["email"], token_decode["tipo"])
                return result
            except TypeError:
                return {"message": "Ocorreu um erro ao alterar o helper!"}, 500
        else: 
            return {"message": "Token de autenticação inválido."}, 401

    @app.route("/HelperDelete", methods=["DELETE"])
    def helper_delete():
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]
            token_decode = valid_token(token)
            try:
                helper_id = request.headers["helperID"]
                result = delete_helper(helper_id, token_decode["tipo"])
                return result
            except TypeError:
                return {"message": "Ocorreu um erro ao excluir o helper!"}, 500
        else: 
            return {"message": "Token de autenticação inválido."}, 401


    @app.route("/HelperList", methods=["GET"])
    def helper_list():
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]
            token_decode = valid_token(token)
            try:
                result = list_helper(token_decode["tipo"])
                return result
            except TypeError:
                return {"message": "Ocorreu um erro ao listar os helper!"}, 500
        else: 
            return {"message": "Token de autenticação inválido."}, 401
