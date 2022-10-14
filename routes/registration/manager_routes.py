from flask import Flask, request

from controllers.auth_controller import valid_token
from controllers.registration.manager_controller import *

def init_app(app: Flask):
    @app.route("/ManagerRegistration", methods=["POST"])
    def manager_register():
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]
            token_decode = valid_token(token)
            try:
                name = request.json["name"]
                email = request.json["email"]
                password = request.json["password"]
                result = registration_manager(name, email, password, token_decode["tipo"])
                return result
            except TypeError:
                return {"message": "Ocorreu um erro ao cadastrar o gestor!"}, 500
        else: 
            return {"message": "Token de autenticação inválido."}, 401

    @app.route("/ManagerEdit", methods=["PUT"])
    def manager_edit():
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]
            token_decode = valid_token(token)
            try:
                manager_id = request.json["managerID"]
                name = request.json["name"]
                email = request.json["email"]
                password = request.json["password"]
                result = edit_manager(manager_id, name, email, password, token_decode["email"], token_decode["tipo"])
                return result
            except TypeError:
                return {"message": "Ocorreu um erro ao alterar o gestor!"}, 500
        else: 
            return {"message": "Token de autenticação inválido."}, 401
    
    @app.route("/ManagerDelete", methods=["DELETE"])
    def manager_delete():
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]
            token_decode = valid_token(token)
            try:
                manager_id = request.headers["managerID"]
                result = delete_manager(manager_id, token_decode["tipo"])
                return result
            except TypeError:
                return {"message": "Ocorreu um erro ao deletar o gestor!"}, 500
        else: 
            return {"message": "Token de autenticação inválido."}, 401


    @app.route("/ManagerList", methods=["GET"])
    def manager_list():
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]
            token_decode = valid_token(token)
            try:
                result = list_manager(token_decode["tipo"])
                return result
            except TypeError:
                return {"message": "Ocorreu um erro ao listar os gestores!"}, 500
        else: 
            return {"message": "Token de autenticação inválido."}, 401
