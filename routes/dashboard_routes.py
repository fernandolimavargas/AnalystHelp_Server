from flask import Flask, request

from controllers.auth_controller import valid_token
from controllers.dashboard_controller import (
    busca_inf_cards_sol,
    busca_inf_filas_gerais,
    busca_inf_filas,
    busca_inf_bases,
    busca_inf_filas_analitic,
    request_bug_create
)


def init_app(app: Flask):
    @app.route("/RequestCardsInformation", methods=["GET"])
    def req_cards_inf():
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]
            token_decode = valid_token(token)
            try:
                return busca_inf_cards_sol(token_decode["id"], token_decode["tipo"])
            except TypeError:
                return {"message": "Ocorreu um erro na atualização dos cards!"}, 500
        else:
            return {"message": "Token de autenticação inválido."}, 401

    @app.route("/GeneralQueuesInformation", methods=["GET"])
    def ger_queues_inf():
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]
            valid_token(token)
            try:
                return busca_inf_filas_gerais()
            except TypeError:
                return {"message": "Ocorreu um erro na atualização do controle de filas!"}, 500
        else:
            return {"message": "Token de autenticação inválido."}, 401

    @app.route("/AnalystQueuesInformationAnalitic", methods=["GET"])
    def inf_filas_analitic():
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]
            token_decode = valid_token(token)
            try:
                return busca_inf_filas_analitic(token_decode["id"], token_decode["tipo"])
            except TypeError:
                return {"message": "O Workflow demorou mais do que o esperado para responder!",
                "erro": ValueError}, 406
        else:
            return {"message": "Token de autenticação inválido."}, 401

    @app.route("/AnalystQueuesInformation", methods=["GET"])
    def ana_queues_inf():
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]
            token_decode = valid_token(token)
            try:
                return busca_inf_filas(token_decode["id"], token_decode["tipo"], token_decode["email"])
            except TypeError:
                return {"message": "Ocorreu um erro na atualização da listagem de TPs!"}, 500
        else:
            return {"message": "Token de autenticação inválido."}, 401


    @app.route("/InformationBases", methods=["GET"])
    def inf_bases():
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]
            valid_token(token)
            try:
                return busca_inf_bases()
            except TypeError:
                return {"message": "Ocorreu um erro na atualização da listagem de bases!"}, 500
        else:
            return {"message": "Token de autenticação inválido."}, 401

    @app.route("/ErrorChangeRequest", methods=["POST"])
    def request_bug():
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]
            token_decode = valid_token(token)
            try:
                systemDoing = request.json["systemDoing"]
                shouldDo = request.json["shouldDo"]
                note = request.json["note"]
                request_type = request.json["requestType"]
                result = request_bug_create(
                    token_decode["id"], systemDoing, shouldDo, note, request_type)
                return result
            except TypeError:
                return {"message": "Ocorreu um erro na solicitação de correção/alteração!"}, 500
        else:
            return {"message": "Token de autenticação inválido."}, 401
