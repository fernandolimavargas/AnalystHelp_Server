from flask import Flask, request

from controllers.auth_controller import valid_token
from controllers.registration.user_controller import *


def init_app(app: Flask):
    @app.route("/UserRegistration", methods=["POST"])
    def user_reg():
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]
            token_decode = valid_token(token)
            try:
                name = request.json["name"]
                email = request.json["email"]
                password = request.json["password"]
                user_type = request.json["userType"]
                goal = request.json["goal"]
                office = request.json["office"]
                committee = request.json["committee"]
                inactive = request.json["inactive"]
                team_id = request.json["team"]
                result = user_registration(name,
                                              email,
                                              password,
                                              user_type,
                                              goal,
                                              office,
                                              committee,
                                              inactive,
                                              team_id,
                                              token_decode["tipo"])
                return result
            except TypeError:
                return {"message": "Ocorreu um erro ao cadastrar o analista!"}, 500
        else:
            return {"message": "Token de autenticação inválido."}, 401

    @app.route("/UserAlteration", methods=["PUT"])
    def user_alt():
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]
            token_decode = valid_token(token)
            try:
                user_id = request.json["userID"]
                name = request.json["name"]
                email = request.json["email"]
                password = request.json["password"]
                user_type = request.json["userType"]
                goal = request.json["goal"]
                office = request.json["office"]
                committee = request.json["committee"]
                inactive = request.json["inactive"]
                team_id = request.json["team"]
                result = user_alteration(user_id,
                                    name,
                                    email,
                                    password,
                                    user_type,
                                    goal,
                                    office,
                                    committee,
                                    inactive,
                                    team_id,
                                    token_decode["email"],
                                    token_decode["tipo"])
                return result
            except TypeError:
                return {"message": "Ocorreu um erro ao alterar o analista!",
                "error": ValueError}, 500
        else:
            return {"message": "Token de autenticação inválido."}, 401

    @app.route("/UserDelete", methods=["DELETE"])
    def user_del():
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]
            token_decode = valid_token(token)
            try:
                user_id = request.headers["userID"]
                user_type_reg = request.headers["type"]
                result = user_delete(user_id, user_type_reg, token_decode["tipo"])
                return result
            except TypeError:
                return {"message": "Ocorreu um erro ao listar os analistas!"}, 500
        else:
            return {"message": "Token de autenticação inválido."}, 401

    @app.route("/UserList", methods=["GET"])
    def user_list():
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]
            token_decode = valid_token(token)
            try:
                user_profile = request.headers["userProfile"]
                result = user_listing(user_profile, token_decode["id"], token_decode["tipo"])
                return result
            except ValueError:
                return {"message": "Ocorreu um erro ao listar os analistas!",
                "error": ValueError}, 500
        else:
            return {"message": "Token de autenticação inválido."}, 401
