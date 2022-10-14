from flask import Flask, request

from controllers.auth_controller import valid_token
from controllers.requests.alteration_request_controller import *

def ini_app(app: Flask): 
    @app.route("/ReqAlteration", methods=["POST"])
    def req_alteration():
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]
            token_decode = valid_token(token)
            try:
                result = True
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
                result = True
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
                result = True
                return result 
            except TypeError:
                return {"message": "Ocorreu um erro ao solicitar informação!"}, 500
        else:
            return {"message":"Token de autenticação inválido."}, 401
            
    @app.route("/ReqAlterationInfRes", methods=["POST"])
    def req_alteration_inf_res():
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]
            token_decode = valid_token(token)
            try:
                result = True
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
                result = True
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
                result = True
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
                result = True 
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
                result = True
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
                result = True
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
                result = True
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
                result = True
                return result 
            except TypeError:
                return {"message": "Ocorreu um erro ao encaminhar a solicitação!"}, 500
        else:
            return {"message": "Token de autenticação inválido."}, 401

    @app.route("/ReqAlterationEdit", methods=["POST"])
    def req_alteration_refer():
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]
            token_decode = valid_token(token)
            try:
                result = True
                return result 
            except TypeError:
                return {"message": "Ocorreu um erro ao alterar a solicitação!"}, 500
        else:
            return {"message": "Token de autenticação inválido."}, 401