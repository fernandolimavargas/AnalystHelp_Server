from flask import Flask, request

from controllers.auth_controller import valid_token
from controllers.requests.error_request_controller import *

def init_app(app: Flask):
    @app.route("/ReqError", methods=["POST"])
    def req_error():
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]
            token_decode = valid_token(token)
            try:
                nro_tp = request.json["nroTp"]
                path_menu = request.json["pathMenu"]
                cod_menu = request.json["codMenu"]
                making = request.json["making"]
                make = request.json["make"]
                alternative = request.json["alternative"]
                link_docs = request.json["linkDocs"]
                base = request.json["base"]
                version = request.json["version"]
                prev_version = request.json["prevVersion"]
                duplicate = request.json["duplicate"]

                result = request_error(nro_tp, 
                    path_menu, 
                    cod_menu, 
                    making, 
                    make, 
                    alternative, 
                    link_docs,
                    base,
                    version,
                    prev_version,
                    token_decode["id"],
                    duplicate)
                return result
            except TypeError:
                return {"message": "Ocorreu um erro ao solicitar a analise!"}, 500
        else:
            return {"message": "Token de autenticação inválido."}, 401

    @app.route("/ReqErrorStart", methods=["POST"])
    def req_error_start():
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]
            token_decode = valid_token(token)
            try:
                id_tp = request.json["idTp"]
                result = request_error_start(id_tp, token_decode["id"], token_decode["tipo"])
                return result
            except TypeError:
                return {"message": "Ocorreu um erro ao iniciar a analise!"}, 500
        else:
            return {"message": "Token de autenticação inválido."}, 401
        
    @app.route("/ReqErrorInf", methods=["POST"])
    def req_error_inf():
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]
            token_decode = valid_token(token)
            try:
                id_tp = request.json["idTp"]
                message = request.json["message"]
                result = request_error_information(id_tp, message, token_decode["id"], token_decode["tipo"])
                return result
            except TypeError:
                return {"message": "Ocorreu um erro ao solicitar informação!"}, 500
        else:
            return {"message": "Token de autenticação inválido."}, 401

    @app.route("/ReqErrorInfRes", methods=["POST"])
    def req_error_inf_res():
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]
            token_decode = valid_token(token)
            try:
                error_id = request.json["idTp"]
                nro_tp = request.json["nroTp"]
                path_menu = request.json["pathMenu"]
                cod_menu = request.json["codMenu"]
                making = request.json["making"]
                make = request.json["make"]
                alternative = request.json["alternative"]
                link_docs = request.json["linkDocs"]
                base = request.json["base"]
                version = request.json["version"]
                prev_version = request.json["prevVersion"]
                message = request.json["message"]

                result = request_error_information_response(error_id,
                    nro_tp, 
                    path_menu, 
                    cod_menu, 
                    making, 
                    make, 
                    alternative, 
                    link_docs,
                    base,
                    version,
                    prev_version,
                    token_decode["id"],
                    message,
                    token_decode["tipo"])
                return result
            except TypeError:
                return {"message": "Ocorreu um erro ao responder a solicitação de informação!"}, 500
        else:
            return {"message": "Token de autenticação inválido."}, 401

    @app.route("/ReqErrorAproved", methods=["POST"])
    def req_error_aproved():
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]
            token_decode = valid_token(token)
            try:
                id_tp = request.json["idTp"]
                message = request.json["message"]
                result = request_error_aproved(id_tp, message, token_decode["id"], token_decode["tipo"])
                return result 
            except TypeError:
                return {"message": "Ocorreu um erro ao aprovar a analise!"}, 500
        else:
            return {"message": "Token de autenticação inválido."}, 401

    @app.route("/ReqErrorMark", methods=["POST"])
    def req_error_mark():
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]
            token_decode = valid_token(token)
            try:
                error_id = request.json["idTp"]
                issue = request.json["issue"]
                result = request_error_mark(error_id, issue, token_decode["id"], token_decode["tipo"])
                return result
            except TypeError:
                return {"message": "Ocorreu um erro ao solicitar o rótulo!"}, 500
        else:
            return {"message": "Token de autenticação inválido."}, 401

    @app.route("/ReqErrorFinished", methods=["POST"])
    def req_error_finished():
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]
            token_decode = valid_token(token)
            try:
                error_id = request.json["idTp"]
                message = request.json["message"]
                result = request_error_finished(error_id, message, token_decode['id'], token_decode["tipo"])
                return result
            except TypeError:
                return {"message": "Ocorreu um erro ao finalizar a solicitação!"}, 500
        else:
            return {"message": "Token de autenticação inválido."}, 401
    
    @app.route("/ReqErrorRecused", methods=["POST"])
    def req_error_recused():
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]
            token_decode = valid_token(token)
            try:
                error_id = request.json["idTp"]
                message = request.json["message"]
                result = request_error_recused(error_id, message, token_decode['id'], token_decode["tipo"])
                return result
            except TypeError:
                return {"message": "Ocorreu um erro ao recusar a solicitação!"}, 500
        else:
            return {"message": "Token de autenticação inválido."}, 401
    
    @app.route("/ReqErrorRefer", methods=["POST"])
    def req_error_refer():
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]
            token_decode = valid_token(token)
            try:
                error_id = request.json["idTp"]
                helper_to_forward = request.json["helperToForward"]
                result = request_error_refer(error_id, token_decode["id"], token_decode["tipo"], helper_to_forward)
                return result
            except TypeError:
                return {"message": "Ocorreu um erro ao encaminhar a solicitação!"}, 500
        else:
            return {"message": "Token de autenticação inválido."}, 401
    
    @app.route("/ReqErrorEdit", methods=["POST"])
    def req_error_edit():
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]
            token_decode = valid_token(token)
            try:
                error_id = request.json["idTp"]
                nro_tp = request.json["nroTp"]
                path_menu = request.json["pathMenu"]
                cod_menu = request.json["codMenu"]
                making = request.json["making"]
                make = request.json["make"]
                alternative = request.json["alternative"]
                link_docs = request.json["linkDocs"]
                base = request.json["base"]
                version = request.json["version"]
                prev_version = request.json["prevVersion"]
                result = request_error_edit(error_id,
                    nro_tp, 
                    path_menu, 
                    cod_menu, 
                    making, 
                    make, 
                    alternative, 
                    link_docs,
                    base,
                    version,
                    prev_version,
                    token_decode["id"],
                    token_decode["tipo"])
                return result
            except TypeError:
                return {"message": "Ocorreu um erro ao alterar a solicitação!"}, 500
        else:
            return {"message": "Token de autenticação inválido."}, 401