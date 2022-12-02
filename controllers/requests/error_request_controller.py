from extensions.database import database
from models.models import USUARIO, SOL_ERRO, TIME, MOV_SOL, NOTIFICACAO
from datetime import datetime


def request_error(nro_tp,
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
                  analyst_id,
                  duplicate):

    error = database.session.query(SOL_ERRO).filter(
        SOL_ERRO.NRO_TP == nro_tp).first()

    if error and not duplicate:
        return {"message": "Já existe uma solicitação de erro para essa TP!"}, 406

    analyst = database.session.query(USUARIO).filter(
        USUARIO.ID == analyst_id).first()
    group = database.session.query(TIME).filter(
        TIME.id == analyst.TIME_ID).first()
    helper = database.session.query(USUARIO).filter(
        USUARIO.ID == group.HELPER_ID).first()

    error = SOL_ERRO(NRO_TP=nro_tp,
                     ISSUE="N",
                     CAMINHO_MENU=path_menu,
                     CODIGO_MENU=cod_menu,
                     FAZENDO=making,
                     FAZER=make,
                     PALIATIVA=alternative,
                     DOCS=link_docs,
                     TIPO_DB=type_db,
                     USER_DB=user_db,
                     BANCO=base,
                     SERVER=server,
                     VERSAO=version,
                     VERSAO_ANT=prev_version,
                     OBS=obs,
                     ANALISTA_ID=analyst_id,
                     HELPER_ID=helper.ID,
                     DTA_CREATE=datetime.now())

    database.session.add(error)

    database.session.commit()

    error = database.session.query(SOL_ERRO).filter(
        SOL_ERRO.NRO_TP == nro_tp).order_by(SOL_ERRO.id.desc()).first()

    mov = MOV_SOL(ID_SOL=error.id,
                  TIPO_SOL='error',
                  TITULO="Abertura de analise",
                  TIPO="A",
                  HELPER="",
                  ANALISTA=analyst.NOME,
                  RESUMO="Solicitação de erro aberta.",
                  STATUS="NÃO INICIADO",
                  DTA_CREATE=datetime.now())

    database.session.add(mov)

    notification = NOTIFICACAO(TIPO="Solicitação",
                                 SUBTIPO="Erro",
                                 MENSAGEM=f"Foi aberta uma solicitação de erro para a TP {nro_tp}.",
                                 USUARIO_ID=helper.ID,
                                 DTA_CREATE=datetime.now())

    database.session.add(notification)

    database.session.commit()

    return {"message": "Solicitação de análise de erro enviada!"}, 200


def request_error_start(error_id, user_id, user_type):
    if user_type != "H":
        return {"message": "Você não tem permissão para realizar essa operação."}, 401

    helper = database.session.query(USUARIO).filter(
        USUARIO.ID == user_id).first()

    error = database.session.query(SOL_ERRO).filter(
        SOL_ERRO.id == error_id).first()

    error.STATUS = "EM ANALISE"

    mov = MOV_SOL(ID_SOL=error.id,
                  TIPO_SOL='error',
                  TITULO="Análise iniciada",
                  TIPO="H",
                  HELPER=helper.NOME,
                  ANALISTA="",
                  RESUMO="Sua analise está em andamento.",
                  STATUS="EM ANALISE",
                  DTA_CREATE=datetime.now())

    database.session.add(mov)

    notification = NOTIFICACAO(TIPO="Solicitação",
                                 SUBTIPO="Erro",
                                 MENSAGEM=f"Sua solicitação de erro para a TP {error.NRO_TP} teve uma interação.",
                                 USUARIO_ID=error.ANALISTA_ID,
                                 DTA_CREATE=datetime.now())

    database.session.add(notification)

    database.session.commit()

    return {"message": "Solicitação de análise de erro inciada."}, 200


def request_error_information(error_id, message, user_id, user_type):
    if user_type != "H":
        return {"message": "Você não tem permissão para realizar essa operação."}, 401

    helper = database.session.query(USUARIO).filter(
        USUARIO.ID == user_id).first()

    error = database.session.query(SOL_ERRO).filter(
        SOL_ERRO.id == error_id).first()

    error.STATUS = "AGUARDANDO INFORMAÇÃO"

    mov = MOV_SOL(ID_SOL=error.id,
                  TIPO_SOL='error',
                  TITULO="Solicitação de Informação",
                  TIPO="H",
                  HELPER=helper.NOME,
                  ANALISTA="",
                  RESUMO=message,
                  STATUS="AGUARDANDO INFORMAÇÃO",
                  DTA_CREATE=datetime.now())

    database.session.add(mov)

    notification = NOTIFICACAO(TIPO="Solicitação",
                                 SUBTIPO="Erro",
                                 MENSAGEM=f"Sua solicitação de erro para a TP {error.NRO_TP} teve uma interação.",
                                 USUARIO_ID=error.ANALISTA_ID,
                                 DTA_CREATE=datetime.now())

    database.session.add(notification)

    database.session.commit()

    return {"message": "Solicitação de informação enviada ao analista."}, 200


def request_error_information_response(error_id,
                                       user_id,
                                       message):

    error = database.session.query(SOL_ERRO).filter(
        SOL_ERRO.id == error_id).first()

    if error.ANALISTA_ID != user_id:
        return {"message": "Você não tem permissão para realizar essa operação."}, 401

    error.STATUS = "EM ANALISE"

    analyst = database.session.query(USUARIO).filter(
        USUARIO.ID == error.ANALISTA_ID).first()

    mov = MOV_SOL(ID_SOL=error.id,
                  TIPO_SOL='error',
                  TITULO="Solicitação de informação respondida",
                  TIPO="A",
                  HELPER="",
                  ANALISTA=analyst.NOME,
                  RESUMO=message,
                  STATUS="EM ANALISE",
                  DTA_CREATE=datetime.now())

    database.session.add(mov)

    notification = NOTIFICACAO(TIPO="Solicitação",
                                 SUBTIPO="Erro",
                                 MENSAGEM=f"Sua solicitação de erro para a TP {error.NRO_TP} teve uma interação.",
                                 USUARIO_ID=error.HELPER_ID,
                                 DTA_CREATE=datetime.now())

    database.session.add(notification)

    database.session.commit()

    return {"message": "Solicitação de informação repondida."}, 200


def request_error_aproved(error_id, message, user_id, user_type):
    if user_type != "H":
        return {"message": "Você não tem permissão para realizar essa operação."}, 401

    helper = database.session.query(USUARIO).filter(
        USUARIO.ID == user_id).first()

    error = database.session.query(SOL_ERRO).filter(
        SOL_ERRO.id == error_id).first()

    error.SOLUCAO = message
    error.STATUS = "AGUARDANDO ABERTURA DE ISSUE"


    mov = MOV_SOL(ID_SOL=error.id,
                  TIPO_SOL='error',
                  TITULO="Aprovada abertura de ISSUE",
                  TIPO="H",
                  HELPER=helper.NOME,
                  ANALISTA="",
                  RESUMO="Solicitação aprovada, não se esqueça de validar a taxonomia da TP antes de enviar para correção.",
                  STATUS="AGUARDANDO ABERTURA DE ISSUE",
                  DTA_CREATE=datetime.now())

    database.session.add(mov)

    notification = NOTIFICACAO(TIPO="Solicitação",
                                 SUBTIPO="Erro",
                                 MENSAGEM=f"Sua solicitação de erro para a TP {error.NRO_TP} teve uma interação.",
                                 USUARIO_ID=error.ANALISTA_ID,
                                 DTA_CREATE=datetime.now())

    database.session.add(notification)

    database.session.commit()

    return {"message": "Solicitação de análise de erro aprovada."}, 200


def request_error_mark(error_id, issue, user_id):
    error = SOL_ERRO.query.filter_by(id=error_id).first()

    if error.ANALISTA_ID != user_id:
        return {"message": "Você não tem permissão para realizar essa operação."}, 401

    analyst = USUARIO.query.filter_by(ID=error.ANALISTA_ID).first()

    error.ISSUE = issue
    error.STATUS = "AGUARDANDO ADIÇÃO DE RÓTULO"

    mov = MOV_SOL(ID_SOL=error.id,
                  TIPO_SOL='error',
                  TITULO="Solicitação de rótulo no JIRA",
                  TIPO="A",
                  HELPER="",
                  ANALISTA=analyst.NOME,
                  RESUMO="ISSUE aberta e informada na solicitação favor adicionar o rótulo.",
                  STATUS="AGUARDANDO ADIÇÃO DE RÓTULO",
                  DTA_CREATE=datetime.now())

    database.session.add(mov)

    notification = NOTIFICACAO(TIPO="Solicitação",
                                 SUBTIPO="Erro",
                                 MENSAGEM=f"Sua solicitação de erro para a TP {error.NRO_TP} teve uma interação.",
                                 USUARIO_ID=error.HELPER_ID,
                                 DTA_CREATE=datetime.now())

    database.session.add(notification)

    database.session.commit()

    return {"message": "Solicitação de adição de rótulo enviada ao helper"}, 200


def request_error_finished(error_id, message, user_id, user_type):
    if user_type != "H":
        return {"message": "Você não tem permissão para realizar essa operação."}, 401

    helper = database.session.query(USUARIO).filter(
        USUARIO.ID == user_id).first()

    error = database.session.query(SOL_ERRO).filter(
        SOL_ERRO.id == error_id).first()

    error.SOLUCAO = message
    error.STATUS = "FINALIZADA"
    error.DTA_CONCLUDED = datetime.now()

    mov = MOV_SOL(ID_SOL=error.id,
                  TIPO_SOL='error',
                  TITULO="Solicitação finalizada",
                  TIPO="H",
                  HELPER=helper.NOME,
                  ANALISTA="",
                  RESUMO="Rótulo adicionado.",
                  STATUS="FINALIZADA",
                  DTA_CREATE=datetime.now())

    database.session.add(mov)

    notification = NOTIFICACAO(TIPO="Solicitação",
                                 SUBTIPO="Erro",
                                 MENSAGEM=f"Sua solicitação de erro para a TP {error.NRO_TP} teve uma interação.",
                                 USUARIO_ID=error.ANALISTA_ID,
                                 DTA_CREATE=datetime.now())

    database.session.add(notification)

    database.session.commit()

    return {"message": "Solicitação finalizada."}, 200


def request_error_reopen(error_id, message, user_id, user_type):
    if user_type != "H":
        return {"message": "Você não tem permissão para realizar essa operação."}, 401

    helper = database.session.query(USUARIO).filter(
        USUARIO.ID == user_id).first()

    error = database.session.query(SOL_ERRO).filter(
        SOL_ERRO.id == error_id).first()

    error.SOLUCAO = message
    error.STATUS = "EM ANALISE"
    error.DTA_CONCLUDED = None

    mov = MOV_SOL(ID_SOL=error.id,
                  TIPO_SOL='error',
                  TITULO="Solicitação Reaberta",
                  TIPO="H",
                  HELPER=helper.NOME,
                  ANALISTA="",
                  RESUMO="Solicitação de erro reaberta.",
                  STATUS="EM ANALISE",
                  DTA_CREATE=datetime.now())

    database.session.add(mov)

    notification = NOTIFICACAO(TIPO="Solicitação",
                                 SUBTIPO="Erro",
                                 MENSAGEM=f"Sua solicitação de erro para a TP {error.NRO_TP} teve uma interação.",
                                 USUARIO_ID=error.ANALISTA_ID,
                                 DTA_CREATE=datetime.now())
                                 

    database.session.add(notification)

    database.session.commit()

    return {"message": "Solicitação reaberta."}, 200


def request_error_recused(error_id, message, user_id, user_type):
    if user_type != "H":
        return {"message": "Você não tem permissão para realizar essa operação."}, 401

    helper = database.session.query(USUARIO).filter(
        USUARIO.ID == user_id).first()

    error = database.session.query(SOL_ERRO).filter(
        SOL_ERRO.id == error_id).first()

    error.SOLUCAO = message
    error.STATUS = "NÃO APROVADO"
    error.DTA_CONCLUDED = datetime.now()

    mov = MOV_SOL(ID_SOL=error.id,
                  TIPO_SOL='error',
                  TITULO="Solicitação recusada",
                  TIPO="H",
                  HELPER=helper.NOME,
                  ANALISTA="",
                  RESUMO="Solicitação não aprovada.",
                  STATUS="NÃO APROVADO",
                  DTA_CREATE=datetime.now())

    database.session.add(mov)

    notification = NOTIFICACAO(TIPO="Solicitação",
                                 SUBTIPO="Erro",
                                 MENSAGEM=f"Sua solicitação de erro para a TP {error.NRO_TP} teve uma interação.",
                                 USUARIO_ID=error.ANALISTA_ID,
                                 DTA_CREATE=datetime.now())

    database.session.add(notification)

    database.session.commit()

    return {"message": "Solicitação recusada."}, 200


def request_error_refer(error_id, user_id, user_type, helper_to_forward):
    if user_type != "H":
        return {"message": "Você não tem permissão para realizar essa operação."}, 401

    helper = database.session.query(USUARIO).filter(
        USUARIO.ID == user_id).first()

    error = database.session.query(SOL_ERRO).filter(
        SOL_ERRO.id == error_id).first()

    helper_refer = database.session.query(USUARIO).filter(
        USUARIO.ID == helper_to_forward).first()

    error.HELPER_ID = helper_to_forward
    error.STATUS = "NÃO INICIADO"

    mov = MOV_SOL(ID_SOL=error.id,
                  TIPO_SOL='error',
                  TITULO="Solicitação encaminhada",
                  TIPO="H",
                  HELPER=helper.NOME,
                  ANALISTA="",
                  RESUMO="Solicitação encaminhada.",
                  STATUS="NÃO INICIADO",
                  DTA_CREATE=datetime.now())

    database.session.add(mov)

    notification = NOTIFICACAO(TIPO="Solicitação",
                                 SUBTIPO="Erro",
                                 MENSAGEM=f"Sua solicitação de erro para a TP {error.NRO_TP} teve uma interação.",
                                 USUARIO_ID=error.ANALISTA_ID,
                                 DTA_CREATE=datetime.now())

    database.session.add(notification)

    notification = NOTIFICACAO(TIPO="Solicitação",
                                 SUBTIPO="Erro",
                                 MENSAGEM=f"Foi encaminhada uma solicitação de erro para a TP {error.NRO_TP}.",
                                 USUARIO_ID=helper_to_forward,
                                 DTA_CREATE=datetime.now())

    database.session.add(notification)

    database.session.commit()

    return {"message": f"Solicitação encaminhada para o helper {helper_refer.NOME}."}, 200


def request_error_edit(error_id,
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
                       user_id,
                       user_type):

    usuario = database.session.query(USUARIO).filter(
        USUARIO.ID == user_id).first()

    error = database.session.query(SOL_ERRO).filter(
        SOL_ERRO.id == error_id).first()

    error.NRO_TP = nro_tp
    error.CAMINHO_MENU = path_menu
    error.CODIGO_MENU = cod_menu
    error.FAZENDO = making
    error.FAZER = make
    error.PALIATIVA = alternative
    error.DOCS = link_docs
    error.TIPO_DB = type_db
    error.USER_DB = user_db
    error.BANCO = base
    error.SERVER = server
    error.VERSAO = version
    error.VERSAO_ANT = prev_version
    error.OBS = obs

    if user_type == 'H':
        mov = MOV_SOL(ID_SOL=error.id,
                    TIPO_SOL='error',
                    TITULO="Solicitação ajustada",
                    TIPO="H",
                    HELPER=usuario.NOME,
                    ANALISTA="",
                    RESUMO="Solicitação ajustada.",
                    STATUS="AJUSTE DE INFORMAÇÃO",
                    DTA_CREATE=datetime.now())
    elif user_type == 'A':
        mov = MOV_SOL(ID_SOL=error.id,
                    TIPO_SOL='error',
                    TITULO="Solicitação ajustada",
                    TIPO="A",
                    HELPER="",
                    ANALISTA=usuario.NOME,
                    RESUMO="Solicitação ajustada.",
                    STATUS="AJUSTE DE INFORMAÇÃO",
                    DTA_CREATE=datetime.now())

    database.session.add(mov)

    if user_type == 'H':
        notification = NOTIFICACAO(TIPO="Solicitação",
                                    SUBTIPO="Erro",
                                    MENSAGEM=f"Sua solicitação de erro para a TP {error.NRO_TP} teve uma interação.",
                                    USUARIO_ID=error.ANALISTA_ID,
                                    DTA_CREATE=datetime.now())
    elif user_type == 'A':
        notification = NOTIFICACAO(TIPO="Solicitação",
                                    SUBTIPO="Erro",
                                    MENSAGEM=f"Sua solicitação de erro para a TP {error.NRO_TP} teve uma interação.",
                                    USUARIO_ID=error.HELPER_ID,
                                    DTA_CREATE=datetime.now())

    database.session.add(notification)

    database.session.commit()

    return {"message": "Solicitação alterada."}, 200


def request_error_list(error_id, user_id, user_type):
    result = []

    if error_id == 'undefined':
        if user_type == "A":
            request_errors = database.session.query(SOL_ERRO).filter(SOL_ERRO.ANALISTA_ID==user_id).all()
        elif user_type == "H":
            request_errors = database.session.query(SOL_ERRO).filter(SOL_ERRO.HELPER_ID==user_id).all()
        elif user_type == "G":
            teams = database.session.query(TIME).filter(TIME.GESTOR_ID==user_id).all()

            list_teams = []

            for i in teams:
                list_teams.append(i.id)

            analysts = USUARIO.query.filter(
                USUARIO.TIME_ID.in_(list_teams)).all()

            list_analyst = []

            for i in analysts:
                list_analyst.append(i.ID)

            request_errors = database.session.query(SOL_ERRO).filter(SOL_ERRO.ANALISTA_ID.in_(list_analyst)).all()
        else:
            request_errors = database.session.query(SOL_ERRO).all()
            
        for error in request_errors[::-1]:
            analyst = database.session.query(USUARIO).filter(
                USUARIO.ID == error.ANALISTA_ID).first()
            helper = database.session.query(USUARIO).filter(
                USUARIO.ID == error.HELPER_ID).first()

            if error.DTA_CONCLUDED:
                date_concluded = error.DTA_CONCLUDED.strftime("%d/%m/%Y %H:%M:%S")
            else: 
                date_concluded = error.DTA_CONCLUDED

            result.append({
                "idError": error.id,
                "nroTP": error.NRO_TP,
                "issue": error.ISSUE,
                "pathMenu": error.CAMINHO_MENU,
                "codMenu": error.CODIGO_MENU,
                "making": error.FAZENDO,
                "make": error.FAZER,
                "paliative": error.PALIATIVA,
                "docs": error.DOCS,
                "typeDb": error.TIPO_DB,
                "userDb": error.USER_DB,
                "dataBase": error.BANCO,
                "server": error.SERVER,
                "version": error.VERSAO,
                "previousVersion": error.VERSAO_ANT,
                "obs": error.OBS,
                "solution": error.SOLUCAO,
                "status": error.STATUS,
                "helperID": error.HELPER_ID,
                "helperName": helper.NOME,
                "analyst": analyst.NOME,
                "analystID": error.ANALISTA_ID,
                "dtaCreate": error.DTA_CREATE.strftime("%d/%m/%Y %H:%M:%S"),
                "dtaConcluded": date_concluded
            })

    else:
        error = database.session.query(SOL_ERRO).filter(SOL_ERRO.id == error_id).first()
        
        analyst = database.session.query(USUARIO).filter(
            USUARIO.ID == error.ANALISTA_ID).first()
        helper = database.session.query(USUARIO).filter(
            USUARIO.ID == error.HELPER_ID).first()
        
        if error.DTA_CONCLUDED:
            date_concluded = error.DTA_CONCLUDED.strftime("%d/%m/%Y %H:%M:%S")
        else: 
            date_concluded = error.DTA_CONCLUDED
    
        result.append({
                    "idError": error.id,
                    "nroTP": error.NRO_TP,
                    "issue": error.ISSUE,
                    "pathMenu": error.CAMINHO_MENU,
                    "codMenu": error.CODIGO_MENU,
                    "making": error.FAZENDO,
                    "make": error.FAZER,
                    "paliative": error.PALIATIVA,
                    "docs": error.DOCS,
                    "typeDb": error.TIPO_DB,
                    "userDb": error.USER_DB,
                    "dataBase": error.BANCO,
                    "server": error.SERVER,
                    "version": error.VERSAO,
                    "previousVersion": error.VERSAO_ANT,
                    "obs": error.OBS,
                    "solution": error.SOLUCAO,
                    "status": error.STATUS,
                    "helperID": error.HELPER_ID,
                    "helperName": helper.NOME,
                    "analyst": analyst.NOME,
                    "analystID": error.ANALISTA_ID,
                    "dtaCreate": error.DTA_CREATE.strftime("%d/%m/%Y %H:%M:%S"),
                    "dtaConcluded": date_concluded
                })
        
    
    return result

def request_error_list_all():
    request_errors = database.session.query(SOL_ERRO).all()

    result = []

    for error in request_errors[::-1]:
        analyst = database.session.query(USUARIO).filter(
            USUARIO.ID == error.ANALISTA_ID).first()
        helper = database.session.query(USUARIO).filter(
            USUARIO.ID == error.HELPER_ID).first()

        if error.DTA_CONCLUDED:
            date_concluded = error.DTA_CONCLUDED.strftime("%d/%m/%Y %H:%M:%S")
        else:
            date_concluded = error.DTA_CONCLUDED

        result.append({
            "idError": error.id,
            "nroTP": error.NRO_TP,
            "issue": error.ISSUE,
            "pathMenu": error.CAMINHO_MENU,
            "codMenu": error.CODIGO_MENU,
            "making": error.FAZENDO,
            "make": error.FAZER,
            "paliative": error.PALIATIVA,
            "docs": error.DOCS,
            "type_db": error.TIPO_DB,
            "userDb": error.USER_DB,
            "dataBase": error.BANCO,
            "server": error.SERVER,
            "version": error.VERSAO,
            "previousVersion": error.VERSAO_ANT,
            "obs": error.OBS,
            "solution": error.SOLUCAO,
            "status": error.STATUS,
            "helperID": error.HELPER_ID,
            "helperName": helper.NOME,
            "analyst": analyst.NOME,
            "analystID": error.ANALISTA_ID,
            "dtaCreate": error.DTA_CREATE.strftime("%d/%m/%Y %H:%M:%S"),
            "dtaConcluded": date_concluded
        })

    return result