from flask import Flask, request

from controllers.auth_controller import valid_token
from controllers.requests.alteration_request_controller import *


def init_app(app: Flask):
    @app.route("/ReqAlteration", methods=["POST"])
    def req_alteration():
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]
            token_decode = valid_token(token)
            try:
                nro_tp = request.json["nroTp"]
                making = request.json["making"]
                make = request.json["make"]
                how = request.json["how"]
                benefit = request.json["benefit"]
                version = request.json["version"]
                docs = request.json["docs"]
                duplicate = request.json["duplicate"]
                result = request_alteration(nro_tp, 
                                            making, 
                                            make, 
                                            how, 
                                            benefit, 
                                            version, 
                                            docs, 
                                            token_decode["id"], 
                                            duplicate)
                return result
            except TypeError:
                return {"message": "Ocorreu um erro ao solicitar a analise!"}, 500
        else:
            return {"message": "Token de autenticação inválido."}, 401

    @app.route("/ReqAlterationStart", methods=["POST"])
    def req_alteration_start():
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]
            token_decode = valid_token(token)
            try:
                id_alteration = request.json["idRequest"]
                result = request_alteration_start(id_alteration, token_decode["id"], token_decode["tipo"])
                return result
            except TypeError:
                return {"message": "Ocorreu um erro ao iniciar a analise!"}, 500
        else:
            return {"message": "Token de autenticação inválido."}, 401

    @app.route("/ReqAlterationInf", methods=["POST"])
    def req_alteration_inf():
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]
            token_decode = valid_token(token)
            try:
                id_alteration = request.json["idRequest"]
                message = request.json["message"]
                result = request_alteration_information(id_alteration, 
                                                        message, 
                                                        token_decode["id"], 
                                                        token_decode["tipo"])
                return result
            except TypeError:
                return {"message": "Ocorreu um erro ao solicitar informação!"}, 500
        else:
            return {"message": "Token de autenticação inválido."}, 401

    @app.route("/ReqAlterationInfRes", methods=["POST"])
    def req_alteration_inf_res():
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]
            token_decode = valid_token(token)
            try:
                id_alteration = request.json["idRequest"]
                nro_tp = request.json["nroTp"]
                making = request.json["making"]
                make = request.json["make"]
                how = request.json["how"]
                benefit = request.json["benefit"]
                version = request.json["version"]
                docs = request.json["docs"]
                message = request.json["message"]
                result = request_alteration_information_response(id_alteration,
                                                                nro_tp,
                                                                making,
                                                                make,
                                                                how,
                                                                benefit,
                                                                version,
                                                                docs,
                                                                message,
                                                                token_decode["id"],
                                                                token_decode["tipo"])
                return result
            except TypeError:
                return {"message": "Ocorreu um erro ao responder a solicitação de informação1!"}, 500
        else:
            return {"message": "Token de autenticação inválido."}, 401

    @app.route("/ReqAlterationHelperAproved", methods=["POST"])
    def req_alteration_helper_aproved():
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]
            token_decode = valid_token(token)
            try:
                id_alteration = request.json["idRequest"]
                message = request.json["message"]
                result = request_alteration_aproved(id_alteration, message, token_decode["id"], token_decode["tipo"])
                return result
            except TypeError:
                return {"message": "Ocorreu um erro ao enviar para análise comitê!"}, 500
        else:
            return {"message": "Token de autenticação inválido."}, 401

    @app.route("/ReqAlterationCommitteeAproved", methods=["POST"])
    def req_alteration_committee_aproved():
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]
            token_decode = valid_token(token)
            try:
                id_alteration = request.json["idRequest"]
                message = request.json["message"]
                result = request_alteration_committee_aproved(id_alteration, message, token_decode["id"], token_decode["tipo"])
                return result
            except TypeError:
                return {"message": "Ocorreu um erro ao aprovar a analise!"}, 500
        else:
            return {"message": "Token de autenticação inválido."}, 401

    @app.route("/ReqAlterationMark", methods=["POST"])
    def req_alteration_mark():
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]
            token_decode = valid_token(token)
            try:
                id_alteration = request.json["idRequest"]
                issue = request.json["issue"]
                result = request_alteration_mark(id_alteration, issue, token_decode["id"], token_decode["tipo"])
                return result
            except TypeError:
                return {"message": "Ocorreu um erro ao solicitar o rótulo!"}, 500
        else:
            return {"message": "Token de autenticação inválido."}, 401

    @app.route("/ReqAlterationFinished", methods=["POST"])
    def req_alteration_finished():
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]
            token_decode = valid_token(token)
            try:
                id_alteration = request.json["idRequest"]
                message = request.json["message"]
                result = request_alteration_finished(id_alteration, message, token_decode["id"], token_decode["tipo"])
                return result
            except TypeError:
                return {"message": "Ocorreu um erro ao finalizar a solicitação!"}, 500
        else:
            return {"message": "Token de autenticação inválido."}, 401

    @app.route("/ReqAlterationHelperRecused", methods=["POST"])
    def req_alteration_helper_recused():
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]
            token_decode = valid_token(token)
            try:
                id_alteration = request.json["idRequest"]
                message = request.json["message"]
                result = request_alteration_recused(id_alteration, message, token_decode["id"], token_decode["tipo"])
                return result
            except TypeError:
                return {"message": "Ocorreu um erro ao recusar a solicitação!"}, 500
        else:
            return {"message": "Token de autenticação inválido."}, 401

    @app.route("/ReqAlterationCommitteeRecused", methods=["POST"])
    def req_alteration_committee_recused():
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]
            token_decode = valid_token(token)
            try:
                id_alteration = request.json["idRequest"]
                message = request.json["message"]
                result = request_alteration_committee_recused(id_alteration, message, token_decode["id"], token_decode["tipo"])
                return result
            except TypeError:
                return {"message": "Ocorreu um erro ao recusar a solicitação!"}, 500
        else:
            return {"message": "Token de autenticação inválido."}, 401

    @app.route("/ReqAlterationRefer", methods=["POST"])
    def req_alteration_refer():
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]
            token_decode = valid_token(token)
            try:
                id_alteration = request.json["idRequest"]
                helper_to_forward = request.json["helperToForward"]
                result = request_alteration_refer(id_alteration, helper_to_forward, token_decode["id"], token_decode["tipo"])
                return result
            except TypeError:
                return {"message": "Ocorreu um erro ao encaminhar a solicitação!"}, 500
        else:
            return {"message": "Token de autenticação inválido."}, 401

    @app.route("/ReqAlterationEdit", methods=["POST"])
    def req_alteration_edit():
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]
            token_decode = valid_token(token)
            try:
                id_alteration = request.json["idRequest"]
                nro_tp = request.json["nroTp"]
                making = request.json["making"]
                make = request.json["make"]
                how = request.json["how"]
                benefit = request.json["benefit"]
                version = request.json["version"]
                docs = request.json["docs"]
                result = request_alteration_edit(id_alteration,
                                                nro_tp,
                                                making,
                                                make,
                                                how,
                                                benefit,
                                                version,
                                                docs,
                                                token_decode["id"],
                                                token_decode["tipo"])
                return result
            except TypeError:
                return {"message": "Ocorreu um erro ao alterar a solicitação!"}, 500
        else:
            return {"message": "Token de autenticação inválido."}, 401

    @app.route("/ReqAlterationList", methods=["GET"])
    def req_alteration_list():
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]
            token_decode = valid_token(token)
            try:
                alteration_id = request.headers["idRequest"]
                result = request_alteration_list(alteration_id, token_decode["id"], token_decode["tipo"])
                return result
            except TypeError:
                return {"message": "Ocorreu um erro ao listar as solicitações!"}, 500
        else:
            return {"message": "Token de autenticação inválido."}, 401

    @app.route("/ReqAlterationListAll", methods=["GET"])
    def req_alteration_list_all():
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]
            valid_token(token)
            try:
                result = request_alteration_list_all()
                return result
            except TypeError:
                return {"message": "Ocorreu um erro ao listar as solicitações!"}, 500
        else:
            return {"message": "Token de autenticação inválido."}, 401