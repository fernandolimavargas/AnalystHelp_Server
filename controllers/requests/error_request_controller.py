from extensions.database import database
from models.models import ANALISTA, SOL_ERRO, HELPER, TIME, MOV_SOL, NOTIFICATIONS, GESTOR


def request_error(nro_tp, 
    path_menu, 
    cod_menu, 
    making, 
    make, 
    alternative, 
    link_docs,
    base,
    version,
    prev_version,
    analyst_id,
    duplicate):
    
    error = database.session.query(SOL_ERRO).filter(SOL_ERRO.NRO_TP==nro_tp).first()

    if error and not duplicate:
        return {"message": "Já existe uma solicitação de erro para essa TP!"}, 201
    
    analyst = database.session.query(ANALISTA).filter(ANALISTA.id==analyst_id).first()
    group = database.session.query(TIME).filter(TIME.id==analyst.TIME_ID).first()
    helper = database.session.query(HELPER).filter(HELPER.id==group.HELPER_ID).first()
    
    error = SOL_ERRO(NRO_TP=nro_tp, 
        ISSUE="N", 
        CAMINHO_MENU=path_menu, 
        CODIGO_MENU=cod_menu, 
        FAZENDO=making, 
        FAZER=make, 
        PALIATIVA=alternative, 
        DOCS=link_docs, 
        BANCO=base, 
        VERSAO=version, 
        VERSAO_ANT=prev_version, 
        ANALISTA_ID=analyst_id, 
        HELPER_ID=helper.id)

    database.session.add(error)

    database.session.commit()

    error = database.session.query(SOL_ERRO).filter(SOL_ERRO.NRO_TP==nro_tp).order_by(SOL_ERRO.id.desc()).first()

    mov = MOV_SOL(ID_SOL=error.id, 
        TIPO_SOL='error',
        TITULO="Abertura de analise", 
        TIPO="A", 
        HELPER="", 
        ANALISTA=analyst.USUARIO,
        RESUMO="Solicitação de erro aberta.", 
        STATUS="AGUARDANDO INICIALIZAÇÂO")

    database.session.add(mov)

    notification = NOTIFICATIONS(TIPO="Solicitação", 
        SUBTIPO="Erro", 
        MENSAGEM=f"Foi aberta uma solicitação de erro para a TP {nro_tp}.",
        HELPER=helper.id)
    
    database.session.add(notification)

    database.session.commit()

    return {"message": "Solicitação de análise de erro enviada com sucesso!"}, 200


def request_error_start(error_id, user_id, user_type):
    if user_type != "H":
        return {"message": "Você não tem permissão para realizar essa operação."}, 401

    helper = database.session.query(HELPER).filter(HELPER.id==user_id).first()    

    error = database.session.query(SOL_ERRO).filter(SOL_ERRO.id==error_id).fisrt()

    error.STATUS = "EM ANALISE"

    mov = MOV_SOL(ID_SOL=error.id, 
        TIPO_SOL='error',
        TITULO="Análise iniciada", 
        TIPO="H", 
        HELPER=helper.USUARIO, 
        ANALISTA="",
        RESUMO="Sua analise está em andamento.", 
        STATUS="EM ANALISE")

    database.session.add(mov)

    notification = NOTIFICATIONS(TIPO="Solicitação", 
        SUBTIPO="Erro", 
        MENSAGEM=f"Sua solicitação de erro para a TP {error.NRO_TP} teve uma interação.",
        ANALISTA=error.ANALISTA_ID)
    
    database.session.add(notification)

    database.session.commit()

    return {"message": "Solicitação de análise de erro inciada."}, 200


def request_error_information(error_id, message, user_id, user_type):
    if user_type != "H":
        return {"message": "Você não tem permissão para realizar essa operação."}, 401

    helper = database.session.query(HELPER).filter(HELPER.id==user_id).first()    
    
    error = database.session.query(SOL_ERRO).filter(SOL_ERRO.id==error_id).fisrt()

    error.STATUS = "AGUARDANDO INFORMAÇÃO"

    mov = MOV_SOL(ID_SOL=error.id, 
        TIPO_SOL='error',
        TITULO="Solicitação de Informação", 
        TIPO="H", 
        HELPER=helper.USUARIO, 
        ANALISTA="",
        RESUMO=message, 
        STATUS="AGUARDANDO INFORMAÇÃO")

    database.session.add(mov)

    notification = NOTIFICATIONS(TIPO="Solicitação", 
        SUBTIPO="Erro", 
        MENSAGEM=f"Sua solicitação de erro para a TP {error.NRO_TP} teve uma interação.",
        ANALISTA=error.ANALISTA_ID)
    
    database.session.add(notification)

    database.session.commit()

    return {"message": "Solicitação de informação enviada ao analista."}, 200


def request_error_information_response(error_id,
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
    user_id,
    message,
    user_type):

    error = database.session.query(SOL_ERRO).filter(SOL_ERRO.id==error_id).first()

    if error.ANALISTA_ID != user_id and user_type != "A":
        return {"message": "Você não tem permissão para realizar essa operação."}, 401

    error.NRO_TP = nro_tp
    error.CAMINHO_MENU = path_menu
    error.CODIGO_MENU = cod_menu
    error.FAZENDO = making
    error.FAZER = make
    error.PALIATIVA = alternative
    error.DOCS = link_docs
    error.BANCO = base
    error.VERSAO = version
    error.VERSAO_ANT = prev_version
    error.STATUS = "EM ANALISE"

    analyst = database.session.query(ANALISTA).filter(ANALISTA.id==error.ANALISTA_ID).fisrt()

    mov = MOV_SOL(ID_SOL=error.id, 
        TIPO_SOL='error', 
        TITULO="Solicitação de informação respondida", 
        TIPO="A", 
        HELPER="", 
        ANALISTA=analyst.USUARIO,
        RESUMO=message, 
        STATUS="AGUARDANDO INFORMAÇÃO")

    database.session.add(mov)

    notification = NOTIFICATIONS(TIPO="Solicitação", 
        SUBTIPO="Erro", 
        MENSAGEM=f"Sua solicitação de erro para a TP {error.NRO_TP} teve uma interação.",
        HELPER=error.HELPER_ID)
    
    database.session.add(notification)

    database.session.commit()


    return {"message": "Solicitação de informação repondida."}, 200


def request_error_aproved(error_id, message, user_id, user_type):
    if user_type != "H":
        return {"message": "Você não tem permissão para realizar essa operação."}, 401

    helper = database.session.query(HELPER).filter(HELPER.id==user_id).first()    

    error = database.session.query(SOL_ERRO).filter(SOL_ERRO.id==error_id).first()

    error.SOLUCAO = message
    error.STATUS = "AGUARDANDO ABERTURA DE ISSUE"

    mov = MOV_SOL(ID_SOL=error.id, 
        TIPO_SOL='error',
        TITULO="Aprovada abertura de ISSUE", 
        TIPO="H", 
        HELPER=helper.USUARIO, 
        ANALISTA="",
        RESUMO="Solicitação aprovada, não se esqueça de validar a taxonomia da TP antes de enviar para correção.", 
        STATUS="AGUARDANDO ABERTURA DE ISSUE")

    database.session.add(mov)

    notification = NOTIFICATIONS(TIPO="Solicitação", 
        SUBTIPO="Erro", 
        MENSAGEM=f"Sua solicitação de erro para a TP {error.NRO_TP} teve uma interação.",
        ANALISTA=error.ANALISTA_ID)
    
    database.session.add(notification)

    database.session.commit()

    return {"message": "Solicitação de análise de erro aprovada."}, 200

def request_error_mark(error_id, issue, user_id, user_type):
    error = SOL_ERRO.query.filter_by(id=error_id).first()

    if error.ANALISTA_ID != user_id and user_type != "A":
        return {"message": "Você não tem permissão para realizar essa operação."}, 401

    analyst = ANALISTA.query.filter_by(id=error.ANALISTA_ID).first()

    error.ISSUE = issue
    error.STATUS = "AGUARDANDO ADIÇÂO DE RÓTULO"

    mov = MOV_SOL(ID_SOL=error.id, 
        TIPO_SOL='error', 
        TITULO="Solicitação de rótulo no JIRA", 
        TIPO="A", 
        HELPER="", 
        ANALISTA=analyst.USUARIO,
        RESUMO="ISSUE aberta e informada na solicitação favor adicionar o rótulo.", 
        STATUS="AGUARDANDO ADIÇÃO DE RÓTULO")

    database.session.add(mov)

    notification = NOTIFICATIONS(TIPO="Solicitação", 
        SUBTIPO="Erro", 
        MENSAGEM=f"Sua solicitação de erro para a TP {error.NRO_TP} teve uma interação.",
        HELPER=error.HELPER_ID)
    
    database.session.add(notification)

    database.session.commit()

    return {"message": "Solicitação de adição de rótulo enviada ao helper"}, 200


def request_error_finished(error_id, message, user_id, user_type):
    if user_type != "H":
        return {"message": "Você não tem permissão para realizar essa operação."}, 401

    helper = database.session.query(HELPER).filter(HELPER.id==user_id).first()    

    error = database.session.query(SOL_ERRO).filter(SOL_ERRO.id==error_id).first()

    error.SOLUCAO = message
    error.STATUS = "FINALIZADA"

    mov = MOV_SOL(ID_SOL=error.id, 
        TIPO_SOL='error',
        TITULO="Solicitação de rótulo no JIRA", 
        TIPO="H", 
        HELPER=helper.USUARIO, 
        ANALISTA="",
        RESUMO="Rótulo adicionado.", 
        STATUS="FINALIZADA")

    database.session.add(mov)

    notification = NOTIFICATIONS(TIPO="Solicitação", 
        SUBTIPO="Erro", 
        MENSAGEM=f"Sua solicitação de erro para a TP {error.NRO_TP} teve uma interação.",
        ANALISTA=error.ANALISTA_ID)
    
    database.session.add(notification)

    database.session.commit()

    return {"message": "Solicitação finalizada."}, 200

def request_error_recused(error_id, message, user_id, user_type):
    if user_type != "H":
        return {"message": "Você não tem permissão para realizar essa operação."}, 401

    helper = database.session.query(HELPER).filter(HELPER.id==user_id).first()    
    
    error = database.session.quert(SOL_ERRO).filter(SOL_ERRO.id==error_id).first()

    error.SOLUCAO = message
    error.STATUS = "NÃO APROVADO"

    mov = MOV_SOL(ID_SOL=error.id, 
        TIPO_SOL='error',
        TITULO="Solicitação recusada", 
        TIPO="H", 
        HELPER=helper.USUARIO, 
        ANALISTA="",
        RESUMO="Solicitação não aprovada.", 
        STATUS="NÃO APROVADO")

    database.session.add(mov)

    notification = NOTIFICATIONS(TIPO="Solicitação", 
        SUBTIPO="Erro", 
        MENSAGEM=f"Sua solicitação de erro para a TP {error.NRO_TP} teve uma interação.",
        ANALISTA=error.ANALISTA_ID)
    
    database.session.add(notification)

    database.session.commit()

    return {"message": "Solicitação recusada."}, 200


def request_error_refer(error_id, user_id, user_type, helper_to_forward):
    if user_type != "H":
        return {"message": "Você não tem permissão para realizar essa operação."}, 401

    helper = database.session.query(HELPER).filter(HELPER.id==user_id).first()    

    error = database.session.query(SOL_ERRO).filter(SOL_ERRO.id==error_id).first()
    
    helper_refer = database.session.query(HELPER).filter(HELPER.id==helper_to_forward).first()

    error.HELPER_ID = helper_to_forward
    error.STATUS = "NÃO INICIADO"

    mov = MOV_SOL(ID_SOL=error.id, 
        TIPO_SOL='error', 
        TITULO="Solicitação encaminhada", 
        TIPO="H", 
        HELPER=helper.USUARIO, 
        ANALISTA="",
        RESUMO="Solicitação encaminhado.", 
        STATUS="NÃO INICIADO")

    database.session.add(mov)

    notification = NOTIFICATIONS(TIPO="Solicitação", 
        SUBTIPO="Erro", 
        MENSAGEM=f"Sua solicitação de erro para a TP {error.NRO_TP} teve uma interação.",
        ANALISTA=error.ANALISTA_ID)
    
    database.session.add(notification)

    notification = NOTIFICATIONS(TIPO="Solicitação", 
        SUBTIPO="Erro", 
        MENSAGEM=f"Foi encaminhada uma solicitação de erro para a TP {error.NRO_TP}.",
        HELPER=helper_to_forward)
    
    database.session.add(notification)

    database.session.commit()

    return {"message": f"Solicitação encaminhada para o helper {helper_refer.USUARIO}."}, 200

def request_error_edit(error_id,
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
    user_id,
    user_type):
    if user_type != "H":
        return {"message": "Você não tem permissão para realizar essa operação."}, 401

    helper = database.session.query(HELPER).filter(HELPER.id==user_id).first() 

    error = database.session.query(SOL_ERRO).filter(SOL_ERRO.id==error_id).first()
    
    error.NRO_TP = nro_tp
    error.CAMINHO_MENU = path_menu
    error.CODIGO_MENU = cod_menu
    error.FAZENDO = making
    error.FAZER = make
    error.PALIATIVA = alternative
    error.DOCS = link_docs
    error.BANCO = base
    error.VERSAO = version
    error.VERSAO_ANT = prev_version

    mov = MOV_SOL(ID_SOL=error.id, 
        TIPO_SOL='error',
        TITULO="Solicitação editada", 
        TIPO="H", 
        HELPER=helper.USUARIO, 
        ANALISTA="",
        RESUMO="Solicitação ajustada.", 
        STATUS="AJUSTE DE INFORMAÇÃO")

    database.session.add(mov)

    notification = NOTIFICATIONS(TIPO="Solicitação", 
        SUBTIPO="Erro", 
        MENSAGEM=f"Sua solicitação de erro para a TP {error.NRO_TP} teve uma interação.",
        ANALISTA=error.ANALISTA_ID)
    
    database.session.add(notification)

    database.session.commit()


    return {"message": "Solicitação alterada."}, 200