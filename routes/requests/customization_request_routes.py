from flask import Flask, request

from controllers.auth_controller import valid_token
from controllers.requests.customization_request_controller import *


def init_app(app: Flask):
    @app.route("/ReqCustomization", methods=["POST"])
    def req_customization():
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
                result = request_customization(nro_tp, 
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

    @app.route("/ReqCustomizationStart", methods=["POST"])
    def req_customization_start():
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]
            token_decode = valid_token(token)
            try:
                id_customization = request.json["idRequest"]
                result = request_customization_start(id_customization, token_decode["id"], token_decode["tipo"])
                return result
            except TypeError:
                return {"message": "Ocorreu um erro ao iniciar a analise!"}, 500
        else:
            return {"message": "Token de autenticação inválido."}, 401

    @app.route("/ReqCustomizationInf", methods=["POST"])
    def req_customization_inf():
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]
            token_decode = valid_token(token)
            try:
                id_customization = request.json["idRequest"]
                message = request.json["message"]
                result = request_customization_information(id_customization, 
                                                        message, 
                                                        token_decode["id"], 
                                                        token_decode["tipo"])
                return result
            except TypeError:
                return {"message": "Ocorreu um erro ao solicitar informação!"}, 500
        else:
            return {"message": "Token de autenticação inválido."}, 401

    @app.route("/ReqCustomizationInfRes", methods=["POST"])
    def req_customization_inf_res():
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]
            token_decode = valid_token(token)
            try:
                id_customization = request.json["idRequest"]
                nro_tp = request.json["nroTp"]
                making = request.json["making"]
                make = request.json["make"]
                how = request.json["how"]
                benefit = request.json["benefit"]
                version = request.json["version"]
                docs = request.json["docs"]
                message = request.json["message"]
                result = request_customization_information_response(id_customization,
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
                return {"message": "Ocorreu um erro ao responder a solicitação de informação!"}, 500
        else:
            return {"message": "Token de autenticação inválido."}, 401

    @app.route("/ReqCustomizationHelperAproved", methods=["POST"])
    def req_customization_helper_aproved():
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]
            token_decode = valid_token(token)
            try:
                id_customization = request.json["idRequest"]
                message = request.json["message"]
                result = request_customization_aproved(id_customization, message, token_decode["id"], token_decode["tipo"])
                return result
            except TypeError:
                return {"message": "Ocorreu um erro ao enviar para análise comitê!"}, 500
        else:
            return {"message": "Token de autenticação inválido."}, 401

    @app.route("/ReqCustomizationCommitteeAproved", methods=["POST"])
    def req_customization_committee_aproved():
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]
            token_decode = valid_token(token)
            try:
                id_customization = request.json["idRequest"]
                message = request.json["message"]
                result = request_customization_committee_aproved(id_customization, message, token_decode["id"], token_decode["tipo"])
                return result
            except TypeError:
                return {"message": "Ocorreu um erro ao aprovar a analise!"}, 500
        else:
            return {"message": "Token de autenticação inválido."}, 401

    @app.route("/ReqCustomizationMark", methods=["POST"])
    def req_customization_mark():
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]
            token_decode = valid_token(token)
            try:
                id_customization = request.json["idRequest"]
                issue = request.json["issue"]
                result = request_customization_mark(id_customization, issue, token_decode["id"], token_decode["tipo"])
                return result
            except TypeError:
                return {"message": "Ocorreu um erro ao solicitar o rótulo!"}, 500
        else:
            return {"message": "Token de autenticação inválido."}, 401

    @app.route("/ReqCustomizationFinished", methods=["POST"])
    def req_customization_finished():
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]
            token_decode = valid_token(token)
            try:
                id_customization = request.json["idRequest"]
                message = request.json["message"]
                result = request_customization_finished(id_customization, message, token_decode["id"], token_decode["tipo"])
                return result
            except TypeError:
                return {"message": "Ocorreu um erro ao finalizar a solicitação!"}, 500
        else:
            return {"message": "Token de autenticação inválido."}, 401

    @app.route("/ReqCustomizationHelperRecused", methods=["POST"])
    def req_customization_helper_recused():
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]
            token_decode = valid_token(token)
            try:
                id_customization = request.json["idRequest"]
                message = request.json["message"]
                result = request_customization_recused(id_customization, message, token_decode["id"], token_decode["tipo"])
                return result
            except TypeError:
                return {"message": "Ocorreu um erro ao recusar a solicitação!"}, 500
        else:
            return {"message": "Token de autenticação inválido."}, 401

    @app.route("/ReqCustomizationCommitteeRecused", methods=["POST"])
    def req_customization_committee_recused():
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]
            token_decode = valid_token(token)
            try:
                id_customization = request.json["idRequest"]
                message = request.json["message"]
                result = request_customization_committee_recused(id_customization, message, token_decode["id"], token_decode["tipo"])
                return result
            except TypeError:
                return {"message": "Ocorreu um erro ao recusar a solicitação!"}, 500
        else:
            return {"message": "Token de autenticação inválido."}, 401

    @app.route("/ReqCustomizationRefer", methods=["POST"])
    def req_customization_refer():
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]
            token_decode = valid_token(token)
            try:
                id_customization = request.json["idRequest"]
                helper_to_forward = request.json["helperToForward"]
                result = request_customization_refer(id_customization, helper_to_forward, token_decode["id"], token_decode["tipo"])
                return result
            except TypeError:
                return {"message": "Ocorreu um erro ao encaminhar a solicitação!"}, 500
        else:
            return {"message": "Token de autenticação inválido."}, 401

    @app.route("/ReqCustomizationEdit", methods=["POST"])
    def req_customization_edit():
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]
            token_decode = valid_token(token)
            try:
                id_customization = request.json["idRequest"]
                nro_tp = request.json["nroTp"]
                making = request.json["making"]
                make = request.json["make"]
                how = request.json["how"]
                benefit = request.json["benefit"]
                version = request.json["version"]
                docs = request.json["docs"]
                result = request_customization_edit(id_customization,
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

    @app.route("/ReqCustomizationList", methods=["GET"])
    def req_customization_list():
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]
            token_decode = valid_token(token)
            try:
                customization_id = request.headers["idRequest"]
                result = request_customization_list(customization_id, token_decode["id"], token_decode["tipo"])
                return result
            except TypeError:
                return {"message": "Ocorreu um erro ao listar as solicitações!"}, 500
        else:
            return {"message": "Token de autenticação inválido."}, 401

    @app.route("/ReqCustomizationListAll", methods=["GET"])
    def req_customization_list_all():
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]
            valid_token(token)
            try:
                result = request_customization_list_all()
                return result
            except TypeError:
                return {"message": "Ocorreu um erro ao listar as solicitações!"}, 500
        else:
            return {"message": "Token de autenticação inválido."}, 401