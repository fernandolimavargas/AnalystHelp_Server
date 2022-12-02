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
                type_db = request.json["typeDb"]
                user_db = request.json["userDb"]
                base = request.json["base"]
                server = request.json["server"]
                version = request.json["version"]
                prev_version = request.json["prevVersion"]
                obs = request.json["obs"]
                duplicate = request.json["duplicate"]

                result = request_error(nro_tp,
                                       path_menu,
                                       cod_menu,
                                       making,
                                       make,
                                       alternative,
                                       link_docs,
                                       type_db,
                                       user_db,
                                       base,
                                       server,
                                       version,
                                       prev_version,
                                       obs,
                                       token_decode["id"],
                                       duplicate)
                return result
            except TypeError:
                return {"message": "Ocorreu um erro ao abrir a solicitação!"}, 500
        else:
            return {"message": "Token de autenticação inválido."}, 401

    @app.route("/ReqErrorStart", methods=["PUT"])
    def req_error_start():
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]
            token_decode = valid_token(token)
            try:
                error_id = request.json["idRequest"]
                result = request_error_start(
                    error_id, token_decode["id"], token_decode["tipo"])
                return result
            except TypeError:
                return {"message": "Ocorreu um erro ao iniciar a solicitação!"}, 500
        else:
            return {"message": "Token de autenticação inválido."}, 401

    @app.route("/ReqErrorInf", methods=["PUT"])
    def req_error_inf():
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]
            token_decode = valid_token(token)
            try:
                error_id = request.json["idRequest"]
                message = request.json["message"]
                result = request_error_information(
                    error_id, message, token_decode["id"], token_decode["tipo"])
                return result
            except TypeError:
                return {"message": "Ocorreu um erro ao solicitar informação!"}, 500
        else:
            return {"message": "Token de autenticação inválido."}, 401

    @app.route("/ReqErrorInfRes", methods=["PUT"])
    def req_error_inf_res():
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]
            token_decode = valid_token(token)
            try:
                error_id = request.json["idRequest"]
                message = request.json["message"]

                result = request_error_information_response(error_id,
                                                            token_decode["id"],
                                                            message)
                return result
            except TypeError:
                return {"message": "Ocorreu um erro ao responder a solicitação de informação!"}, 500
        else:
            return {"message": "Token de autenticação inválido."}, 401

    @app.route("/ReqErrorAproved", methods=["PUT"])
    def req_error_aproved():
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]
            token_decode = valid_token(token)
            try:
                error_id = request.json["idRequest"]
                message = request.json["message"]
                result = request_error_aproved(
                    error_id, message, token_decode["id"], token_decode["tipo"])
                return result
            except TypeError:
                return {"message": "Ocorreu um erro ao aprovar a solicitação!"}, 500
        else:
            return {"message": "Token de autenticação inválido."}, 401

    @app.route("/ReqErrorReopen", methods=["PUT"])
    def req_error_reopen():
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]
            token_decode = valid_token(token)
            try:
                error_id = request.json["idRequest"]
                message = request.json["message"]
                result = request_error_reopen(
                    error_id, message, token_decode["id"], token_decode["tipo"])
                return result
            except TypeError:
                return {"message": "Ocorreu um erro ao reabrir a solicitação!"}, 500
        else:
            return {"message": "Token de autenticação inválido."}, 401


    @app.route("/ReqErrorMark", methods=["PUT"])
    def req_error_mark():
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]
            token_decode = valid_token(token)
            try:
                error_id = request.json["idRequest"]
                issue = request.json["issue"]
                result = request_error_mark(
                    error_id, issue, token_decode["id"])
                return result
            except TypeError:
                return {"message": "Ocorreu um erro ao solicitar o rótulo!"}, 500
        else:
            return {"message": "Token de autenticação inválido."}, 401

    @app.route("/ReqErrorFinished", methods=["PUT"])
    def req_error_finished():
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]
            token_decode = valid_token(token)
            try:
                error_id = request.json["idRequest"]
                message = request.json["message"]
                result = request_error_finished(
                    error_id, message, token_decode['id'], token_decode["tipo"])
                return result
            except TypeError:
                return {"message": "Ocorreu um erro ao finalizar a solicitação!"}, 500
        else:
            return {"message": "Token de autenticação inválido."}, 401

    @app.route("/ReqErrorRecused", methods=["PUT"])
    def req_error_recused():
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]
            token_decode = valid_token(token)
            try:
                error_id = request.json["idRequest"]
                message = request.json["message"]
                result = request_error_recused(
                    error_id, message, token_decode['id'], token_decode["tipo"])
                return result
            except TypeError:
                return {"message": "Ocorreu um erro ao recusar a solicitação!"}, 500
        else:
            return {"message": "Token de autenticação inválido."}, 401

    @app.route("/ReqErrorRefer", methods=["PUT"])
    def req_error_refer():
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]
            token_decode = valid_token(token)
            try:
                error_id = request.json["idRequest"]
                helper_to_forward = request.json["helperToForward"]
                result = request_error_refer(
                    error_id, token_decode["id"], token_decode["tipo"], helper_to_forward)
                return result
            except TypeError:
                return {"message": "Ocorreu um erro ao encaminhar a solicitação!"}, 500
        else:
            return {"message": "Token de autenticação inválido."}, 401

    @app.route("/ReqErrorEdit", methods=["PUT"])
    def req_error_edit():
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]
            token_decode = valid_token(token)
            try:
                error_id = request.json["idRequest"]
                nro_tp = request.json["nroTp"]
                path_menu = request.json["pathMenu"]
                cod_menu = request.json["codMenu"]
                making = request.json["making"]
                make = request.json["make"]
                alternative = request.json["alternative"]
                link_docs = request.json["linkDocs"]
                type_db = request.json["typeDb"]
                user_db = request.json["userDb"]
                base = request.json["base"]
                server = request.json["server"]
                version = request.json["version"]
                prev_version = request.json["prevVersion"]
                obs = request.json["obs"]
                result = request_error_edit(error_id,
                                            nro_tp,
                                            path_menu,
                                            cod_menu,
                                            making,
                                            make,
                                            alternative,
                                            link_docs,
                                            type_db,
                                            user_db,
                                            base,
                                            server,
                                            version,
                                            prev_version,
                                            obs,
                                            token_decode["id"],
                                            token_decode["tipo"])
                return result
            except TypeError:
                return {"message": "Ocorreu um erro ao alterar a solicitação!"}, 500
        else:
            return {"message": "Token de autenticação inválido."}, 401

    @app.route("/ReqErrorList", methods=["GET"])
    def req_error_list():
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]
            token_decode = valid_token(token)
            try:
                error_id = request.headers["idRequest"]
                result = request_error_list(error_id, token_decode["id"],token_decode["tipo"])
                return result
            except ValueError:
                return {"message": "Ocorreu um erro ao listar as solicitações!"}, 500
        else:
            return {"message": "Token de autenticação inválido."}, 401

    @app.route("/ReqErrorListAll", methods=["GET"])
    def req_error_list_all():
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]
            valid_token(token)
            try:
                result = request_error_list_all()
                return result
            except TypeError:
                return {"message": "Ocorreu um erro ao listar as solicitações!",
                "error": ValueError}, 500
        else:
            return {"message": "Token de autenticação inválido."}, 401