from flask import Flask, request

from controllers.auth_controller import valid_token
from controllers.registration.analysts_controller import *

def init_app(app: Flask):
    @app.route("/AnalystRegistration", methods=["POST"])
    def reg_analysts():
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]
            token_decode = valid_token(token)
            try:
                name = request.json["name"]
                email = request.json["email"]
                password = request.json["password"]
                office = request.json["office"]
                goal = request.json["goal"]
                team_id = request.json["team"]
                result = registration_analyst(name, 
                    email, 
                    password, 
                    office, 
                    goal, 
                    team_id, 
                    token_decode["tipo"])
                return result
            except TypeError:
                return {"message": "Ocorreu um erro ao cadastrar o analista!"}, 500
        else: 
            return {"message": "Token de autenticação inválido."}, 401

    @app.route("/AnalystEdit", methods=["PUT"])
    def analyst_edit():
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]
            token_decode = valid_token(token)
            try:
                analyst_id = request.json["analystID"]
                name = request.json["name"]
                email = request.json["email"]
                password = request.json["password"]
                office = request.json["office"]
                goal = request.json["goal"]
                team_id = request.json["team"]
                result = edit_analyst(analyst_id,
                    name, 
                    email, 
                    password, 
                    office, 
                    goal, 
                    team_id, 
                    token_decode["email"],
                    token_decode["tipo"])
                return result
            except TypeError:
                return {"message": "Ocorreu um erro ao alterar o analista!"}, 500
        else: 
            return {"message": "Token de autenticação inválido."}, 401

    @app.route("/AnalystDelete", methods=["DELETE"])
    def analysts_delete():
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]
            token_decode = valid_token(token)
            try:
                analyst_id = request.headers["analystID"]
                result = delete_analyst(analyst_id, token_decode["tipo"])
                return result
            except TypeError:
                return {"message": "Ocorreu um erro ao listar os analistas!"}, 500
        else: 
            return {"message": "Token de autenticação inválido."}, 401



    @app.route("/AnalystList", methods=["GET"])
    def analysts_list():
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]
            token_decode = valid_token(token)
            try:
                result = list_analyst(token_decode["tipo"])
                return result
            except TypeError:
                return {"message": "Ocorreu um erro ao listar os analistas!"}, 500
        else: 
            return {"message": "Token de autenticação inválido."}, 401
