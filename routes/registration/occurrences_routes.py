from flask import Flask, request

from controllers.auth_controller import valid_token
from controllers.registration.occurrences_controller import *


def init_app(app: Flask):
    @app.route("/OccurrencesRegistration", methods=["POST"])
    def occurrences_register():
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]
            token_decode = valid_token(token)
            try:
                user_id = request.json["userID"]
                oc_type = request.json["ocType"]
                oc_period = request.json["ocPeriod"]
                note = request.json["note"]
                dta_start = request.json["dtaStart"]
                dta_end = request.json["dtaEnd"]
                result = registration_occurrences(
                    user_id, oc_type, oc_period, note, dta_start, dta_end, token_decode["tipo"])
                return result
            except TypeError:
                return {"message": "Ocorreu um erro ao registrar a ocorrencia!"}, 500
        else:
            return {"message": "Token de autenticação inválido."}, 401

    @app.route("/OccurrencesEdit", methods=["PUT"])
    def occurrences_edit():
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]
            token_decode = valid_token(token)
            try:
                occurrence_id = request.json["occurrenceID"]
                user_id = request.json["userID"]
                oc_type = request.json["ocType"]
                oc_period = request.json["ocPeriod"]
                note = request.json["note"]
                dta_start = request.json["dtaStart"]
                dta_end = request.json["dtaEnd"]
                result = edit_occurrences(
                    occurrence_id, user_id, oc_type, oc_period, note, dta_start, dta_end, token_decode["tipo"])
                return result
            except TypeError:
                return {"message": "Ocorreu um erro ao alterar a ocorrencia!"}, 500
        else:
            return {"message": "Token de autenticação inválido."}, 401

    @app.route("/OccurrencesDelete", methods=["DELETE"])
    def occurrences_delete():
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]
            token_decode = valid_token(token)
            try:
                occurrence_id = request.headers["occurrenceID"]
                result = delete_occurrences(
                    occurrence_id, token_decode["tipo"])
                return result
            except TypeError:
                return {"message": "Ocorreu um erro ao deletar a ocorrencia!"}, 500
        else:
            return {"message": "Token de autenticação inválido."}, 401

    @app.route("/OccurrencesList", methods=["GET"])
    def occurrences_list():
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]
            token_decode = valid_token(token)
            try:
                user_id = request.headers["userID"]
                result = list_occurrences(user_id, token_decode["tipo"])
                return result
            except TypeError:
                return {"message": "Ocorreu um erro ao listar as ocorrencias!"}, 500
        else:
            return {"message": "Token de autenticação inválido."}, 401
