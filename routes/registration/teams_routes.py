from flask import Flask, request

from controllers.auth_controller import valid_token
from controllers.registration.team_controller import *

def init_app(app: Flask):
    @app.route("/TeamsRegistration", methods=["POST"])
    def team_register():
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]
            token_decode = valid_token(token)
            try:
                name = request.json["name"]
                helper_id = request.json["helperID"]
                manager_id = request.json["managerID"]
                result = registration_team(name, helper_id, manager_id, token_decode["tipo"])
                return result
            except TypeError:
                return {"message": "Ocorreu um erro ao cadastrar o time!"}, 500
        else: 
            return {"message": "Token de autenticação inválido."}, 401

    @app.route("/TeamsEdit", methods=["PUT"])
    def team_edit():
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]
            token_decode = valid_token(token)
            try:
                team_id = request.json["teamID"]
                name = request.json["name"]
                helper_id = request.json["helperID"]
                manager_id = request.json["managerID"]
                result = edit_team(team_id, name, helper_id, manager_id, token_decode["tipo"])
                return result
            except TypeError:
                return {"message": "Ocorreu um erro ao alterar o time!"}, 500
        else: 
            return {"message": "Token de autenticação inválido."}, 401

    @app.route("/TeamsDelete", methods=["DELETE"])
    def team_delete():
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]
            token_decode = valid_token(token)
            try:
                team_id = request.headers["teamID"]
                result = delete_team(team_id, token_decode["tipo"])
                return result
            except TypeError:
                return {"message": "Ocorreu um erro ao listar os times!"}, 500
        else: 
            return {"message": "Token de autenticação inválido."}, 401


    @app.route("/TeamsList", methods=["GET"])
    def team_list():
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]
            token_decode = valid_token(token)
            try:
                result = list_teams(token_decode["tipo"])
                return result
            except TypeError:
                return {"message": "Ocorreu um erro ao listar os times!"}, 500
        else: 
            return {"message": "Token de autenticação inválido."}, 401
