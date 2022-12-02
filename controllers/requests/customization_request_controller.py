from extensions.database import database
from models.models import USUARIO, SOL_CUSTOMIZACAO, TIME, MOV_SOL, NOTIFICACAO
from datetime import datetime

def request_customization(nro_tp, 
                        making, 
                        make, 
                        how, 
                        benefit, 
                        version, 
                        docs, 
                        analyst_id, 
                        duplicate):

    customization = database.session.query(SOL_CUSTOMIZACAO).filter(SOL_CUSTOMIZACAO.NRO_TP == nro_tp)

    if customization and not duplicate:
        return {"message": "Já existe uma solicitação de customização para essa TP!"}, 406
    
    analyst = database.session.query(USUARIO).filter(
        USUARIO.ID == analyst_id).first()
    group = database.session.query(TIME).filter(
        TIME.id == analyst.TIME_ID).first()
    helper = database.session.query(USUARIO).filter(
        USUARIO.ID == group.HELPER_ID).first()

    customization = SOL_CUSTOMIZACAO(NRO_TP=nro_tp,
                               ISSUE="N",
                               FAZENDO=making,
                               FAZER=make,
                               COMO=how,
                               BENEFICIO=benefit,
                               VERSAO=version,
                               DOCS=docs,
                               ANALISTA_ID=analyst_id,
                               HELPER_ID=helper.ID,
                               DTA_CREATE=datetime.now())
    
    database.session.add(customization)

    database.session.commit()

    customization = database.session.query(SOL_CUSTOMIZACAO).filter(
        SOL_CUSTOMIZACAO.NRO_TP == nro_tp).order_by(SOL_CUSTOMIZACAO.id.desc()).first()

    mov = MOV_SOL(ID_SOL=customization.id,
                  TIPO_SOL='customization',
                  TITULO="Abertura de analise",
                  TIPO="A",
                  HELPER="",
                  ANALISTA=analyst.NOME,
                  RESUMO="Solicitação de customização aberta.",
                  STATUS="AGUARDANDO INICIALIZAÇÃO",
                  DTA_CREATE=datetime.now())

    database.session.add(mov)

    notification = NOTIFICACAO(TIPO="Solicitação",
                                 SUBTIPO="Customização",
                                 MENSAGEM=f"Foi aberta uma solicitação de customização para a TP {nro_tp}.",
                                 USUARIO_ID=helper.ID,
                                 DTA_CREATE=datetime.now())

    database.session.add(notification)

    database.session.commit()


    return {"message": "Solicitação de análise de customização enviada!"}, 200

def request_customization_start(customization_id, user_id, user_type):
    if user_type != "H":
        return {"message": "Você não tem permissão para realizar essa operação."}, 401

    helper = database.session.query(USUARIO).filter(
        USUARIO.ID == user_id).first()
    
    customization = database.session.query(SOL_CUSTOMIZACAO).filter(
        SOL_CUSTOMIZACAO.id == customization_id).first()

    customization.STATUS = "EM ANALISE"

    mov = MOV_SOL(ID_SOL=customization.id,
                  TIPO_SOL='customization',
                  TITULO="Análise iniciada",
                  TIPO="H",
                  HELPER=helper.NOME,
                  ANALISTA="",
                  RESUMO="Sua analise está em andamento.",
                  STATUS="EM ANALISE",
                  DTA_CREATE=datetime.now())

    database.session.add(mov)

    notification = NOTIFICACAO(TIPO="Solicitação",
                                 SUBTIPO="Customização",
                                 MENSAGEM=f"Sua solicitação de customização para a TP {customization.NRO_TP} teve uma interação.",
                                 USUARIO_ID=customization.ANALISTA_ID,
                                 DTA_CREATE=datetime.now())

    database.session.add(notification)

    database.session.commit()


    return {"message": "Solicitação de análise de customização iniciada!"}, 200

def request_customization_information(customization_id, message, user_id, user_type):
    if user_type != "H":
        return {"message": "Você não tem permissão para realizar essa operação."}, 401
    
    
    helper = database.session.query(USUARIO).filter(
        USUARIO.ID == user_id).first()

    customization = database.session.query(SOL_CUSTOMIZACAO).filter(
        SOL_CUSTOMIZACAO.id == customization_id).first()

    customization.STATUS = "AGUARDANDO INFORMAÇÃO"

    mov = MOV_SOL(ID_SOL=customization.id,
                  TIPO_SOL='customization',
                  TITULO="Solicitação de Informação",
                  TIPO="H",
                  HELPER=helper.NOME,
                  ANALISTA="",
                  RESUMO=message,
                  STATUS="AGUARDANDO INFORMAÇÃO",
                  DTA_CREATE=datetime.now())

    database.session.add(mov)

    notification = NOTIFICACAO(TIPO="Solicitação",
                                 SUBTIPO="Customização",
                                 MENSAGEM=f"Sua solicitação de customização para a TP {customization.NRO_TP} teve uma interação.",
                                 USUARIO_ID=customization.ANALISTA_ID,
                                 DTA_CREATE=datetime.now())

    database.session.add(notification)

    database.session.commit()

    return {"message": "Solicitação de informação enviada ao analista."}, 200

def request_customization_information_response(customization_id,
                                            nro_tp,
                                            making,
                                            make,
                                            how,
                                            benefit,
                                            version,
                                            docs,
                                            message,
                                            user_id,
                                            user_type):
    customization = database.session.query(SOL_CUSTOMIZACAO).filter(
        SOL_CUSTOMIZACAO.id == customization_id).first()

    if customization.ANALISTA_ID != user_id and user_type != "A":
        return {"message": "Você não tem permissão para realizar essa operação."}, 401

    customization.NRO_TP = nro_tp
    customization.FAZENDO = making
    customization.FAZER = make
    customization.COMO = how
    customization.BENEFICIO = benefit
    customization.VERSION = version
    customization.DOCS = docs
    customization.STATUS = "EM ANALISE"

    analyst = database.session.query(USUARIO).filter(
        USUARIO.ID == customization.ANALISTA_ID).first()

    mov = MOV_SOL(ID_SOL=customization.id,
                  TIPO_SOL='customization',
                  TITULO="Solicitação de informação respondida",
                  TIPO="A",
                  HELPER="",
                  ANALISTA=analyst.NOME,
                  RESUMO=message,
                  STATUS="AGUARDANDO INFORMAÇÃO",
                  DTA_CREATE=datetime.now())

    database.session.add(mov)

    notification = NOTIFICACAO(TIPO="Solicitação",
                                 SUBTIPO="Customização",
                                 MENSAGEM=f"Sua solicitação de customização para a TP {customization.NRO_TP} teve uma interação.",
                                 USUARIO_ID=customization.HELPER_ID,
                                 DTA_CREATE=datetime.now())

    database.session.add(notification)

    database.session.commit()

    return {"message": "Solicitação de informação repondida."}, 200

def request_customization_aproved(customization_id, message, user_id, user_type):
    if user_type != "H":
        return {"message": "Você não tem permissão para realizar essa operação."}, 401

    helper = database.session.query(USUARIO).filter(
        USUARIO.ID == user_id).first()

    customization = database.session.query(SOL_CUSTOMIZACAO).filter(
        SOL_CUSTOMIZACAO.id == customization_id).first()

    customization.SOLUCAO = message
    customization.STATUS = "ANALISE COMITE"

    mov = MOV_SOL(ID_SOL=customization.id,
                  TIPO_SOL='customization',
                  TITULO="Enviada para analise comite",
                  TIPO="H",
                  HELPER=helper.NOME,
                  ANALISTA="",
                  RESUMO="Solicitação foi para aprovação do comite",
                  STATUS="ANALISE COMITE",
                  DTA_CREATE=datetime.now())

    database.session.add(mov)

    notification = NOTIFICACAO(TIPO="Solicitação",
                                 SUBTIPO="Customização",
                                 MENSAGEM=f"Sua solicitação de customização para a TP {customization.NRO_TP} teve uma interação.",
                                 USUARIO_ID=customization.ANALISTA_ID,
                                 DTA_CREATE=datetime.now())

    database.session.add(notification)

    database.session.commit()

    return {"message": "Solicitação de análise de customização foi para analise comite."}, 200


def request_customization_committee_aproved(customization_id, message, user_id, user_type):
    if user_type != "H":
        return {"message": "Você não tem permissão para realizar essa operação."}, 401

    helper = database.session.query(USUARIO).filter(
        USUARIO.ID == user_id).first()

    customization = database.session.query(SOL_CUSTOMIZACAO).filter(
        SOL_CUSTOMIZACAO.id == customization_id).first()

    customization.SOLUCAO = message
    customization.STATUS = "AGUARDANDO ABERTURA DE ISSUE"

    mov = MOV_SOL(ID_SOL=customization.id,
                  TIPO_SOL='customization',
                  TITULO="Aprovada abertura de ISSUE",
                  TIPO="H",
                  HELPER=helper.NOME,
                  ANALISTA="",
                  RESUMO="Solicitação aprovada, não se esqueça de validar a taxonomia da TP antes de enviar para customização.",
                  STATUS="AGUARDANDO ABERTURA DE ISSUE",
                  DTA_CREATE=datetime.now())

    database.session.add(mov)

    notification = NOTIFICACAO(TIPO="Solicitação",
                                 SUBTIPO="customização",
                                 MENSAGEM=f"Sua solicitação de customização para a TP {customization.NRO_TP} teve uma interação.",
                                 USUARIO_ID=customization.ANALISTA_ID,
                                 DTA_CREATE=datetime.now())

    database.session.add(notification)

    database.session.commit()

    return {"message": "Solicitação de análise de customização aprovada."}, 200

def request_customization_mark(customization_id, issue, user_id, user_type):
    customization = database.session.query(SOL_CUSTOMIZACAO).filter(SOL_CUSTOMIZACAO.id == customization_id).first()

    if customization.ANALISTA_ID != user_id and user_type != "A":
        return {"message": "Você não tem permissão para realizar essa operação."}, 401

    analyst = USUARIO.query.filter_by(ID=customization.ANALISTA_ID).first()

    customization.ISSUE = issue
    customization.STATUS = "AGUARDANDO ADIÇÃO DE RÓTULO"

    mov = MOV_SOL(ID_SOL=customization.id,
                  TIPO_SOL='customization',
                  TITULO="Solicitação de rótulo no JIRA",
                  TIPO="A",
                  HELPER="",
                  ANALISTA=analyst.NOME,
                  RESUMO="ISSUE aberta e informada na solicitação favor adicionar o rótulo.",
                  STATUS="AGUARDANDO ADIÇÃO DE RÓTULO",
                  DTA_CREATE=datetime.now())

    database.session.add(mov)

    notification = NOTIFICACAO(TIPO="Solicitação",
                                 SUBTIPO="Customização",
                                 MENSAGEM=f"Sua solicitação de customização para a TP {customization.NRO_TP} teve uma interação.",
                                 USUARIO_ID=customization.HELPER_ID,
                                 DTA_CREATE=datetime.now())

    database.session.add(notification)

    database.session.commit()

    return {"message": "Solicitação de adição de rótulo enviada ao comite"}, 200

def request_customization_finished(customization_id, message, user_id, user_type):
    if user_type != "H":
        return {"message": "Você não tem permissão para realizar essa operação."}, 401

    helper = database.session.query(USUARIO).filter(
        USUARIO.ID == user_id).first()

    customization = database.session.query(SOL_CUSTOMIZACAO).filter(
        SOL_CUSTOMIZACAO.id == customization_id).first()

    customization.SOLUCAO = message
    customization.STATUS = "FINALIZADA"
    customization.DTA_CONCLUDED = datetime.now()

    mov = MOV_SOL(ID_SOL=customization.id,
                  TIPO_SOL='customization',
                  TITULO="Solicitação de rótulo no JIRA",
                  TIPO="H",
                  HELPER=helper.NOME,
                  ANALISTA="",
                  RESUMO="Rótulo adicionado.",
                  STATUS="FINALIZADA",
                  DTA_CREATE=datetime.now())

    database.session.add(mov)

    notification = NOTIFICACAO(TIPO="Solicitação",
                                 SUBTIPO="Customização",
                                 MENSAGEM=f"Sua solicitação de customização para a TP {customization.NRO_TP} teve uma interação.",
                                 USUARIO_ID=customization.ANALISTA_ID,
                                 DTA_CREATE=datetime.now())

    database.session.add(notification)

    database.session.commit()

    return {"message": "Solicitação finalizada."}, 200

def request_customization_recused(customization_id, message, user_id, user_type):
    if user_type != "H":
        return {"message": "Você não tem permissão para realizar essa operação."}, 401

    helper = database.session.query(USUARIO).filter(
        USUARIO.ID == user_id).first()

    customization = database.session.query(SOL_CUSTOMIZACAO).filter(
        SOL_CUSTOMIZACAO.id == customization_id).first()

    customization.SOLUCAO = message
    customization.STATUS = "NÃO APROVADO"
    customization.DTA_CONCLUDED = datetime.now()

    mov = MOV_SOL(ID_SOL=customization.id,
                  TIPO_SOL='customization',
                  TITULO="Solicitação recusada",
                  TIPO="H",
                  HELPER=helper.NOME,
                  ANALISTA="",
                  RESUMO="Solicitação não aprovada.",
                  STATUS="NÃO APROVADO",
                  DTA_CREATE=datetime.now())

    database.session.add(mov)

    notification = NOTIFICACAO(TIPO="Solicitação",
                                 SUBTIPO="Customização",
                                 MENSAGEM=f"Sua solicitação de customização para a TP {customization.NRO_TP} teve uma interação.",
                                 USUARIO_ID=customization.ANALISTA_ID,
                                 DTA_CREATE=datetime.now())

    database.session.add(notification)

    database.session.commit()

    return {"message": "Solicitação recusada."}, 200

def request_customization_committee_recused(customization_id, message, user_id, user_type):
    if user_type != "H":
        return {"message": "Você não tem permissão para realizar essa operação."}, 401

    helper = database.session.query(USUARIO).filter(
        USUARIO.ID == user_id).first()

    customization = database.session.query(SOL_CUSTOMIZACAO).filter(
        SOL_CUSTOMIZACAO.id == customization_id).first()

    customization.SOLUCAO = message
    customization.STATUS = "NÃO APROVADO COMITE"
    customization.DTA_CONCLUDED = datetime.now()

    mov = MOV_SOL(ID_SOL=customization.id,
                  TIPO_SOL='customization',
                  TITULO="Solicitação recusada",
                  TIPO="H",
                  HELPER=helper.NOME,
                  ANALISTA="",
                  RESUMO="Solicitação não aprovada.",
                  STATUS="NÃO APROVADO COMITE",
                  DTA_CREATE=datetime.now())

    database.session.add(mov)

    notification = NOTIFICACAO(TIPO="Solicitação",
                                 SUBTIPO="Customização",
                                 MENSAGEM=f"Sua solicitação de customização para a TP {customization.NRO_TP} teve uma interação.",
                                 USUARIO_ID=customization.ANALISTA_ID,
                                 DTA_CREATE=datetime.now())

    database.session.add(notification)

    database.session.commit()

    return {"message": "Solicitação recusada."}, 200

def request_customization_refer(customization_id, helper_to_forward, user_id, user_type):
    if user_type != "H":
        return {"message": "Você não tem permissão para realizar essa operação."}, 401

    helper = database.session.query(USUARIO).filter(
        USUARIO.ID == user_id).first()

    customization = database.session.query(SOL_CUSTOMIZACAO).filter(
        SOL_CUSTOMIZACAO.id == customization_id).first()

    helper_refer = database.session.query(USUARIO).filter(
        USUARIO.ID == helper_to_forward).first()

    customization.HELPER_ID = helper_to_forward
    customization.STATUS = "NÃO INICIADO"

    mov = MOV_SOL(ID_SOL=customization.id,
                  TIPO_SOL='customization',
                  TITULO="Solicitação encaminhada",
                  TIPO="H",
                  HELPER=helper.NOME,
                  ANALISTA="",
                  RESUMO="Solicitação encaminhado.",
                  STATUS="NÃO INICIADO",
                  DTA_CREATE=datetime.now())

    database.session.add(mov)

    notification = NOTIFICACAO(TIPO="Solicitação",
                                 SUBTIPO="Customização",
                                 MENSAGEM=f"Sua solicitação de customização para a TP {customization.NRO_TP} teve uma interação.",
                                 USUARIO_ID=customization.ANALISTA_ID,
                                 DTA_CREATE=datetime.now())

    database.session.add(notification)

    notification = NOTIFICACAO(TIPO="Solicitação",
                                 SUBTIPO="Customização",
                                 MENSAGEM=f"Foi encaminhada uma solicitação de customização para a TP {customization.NRO_TP}.",
                                 USUARIO_ID=helper_to_forward,
                                 DTA_CREATE=datetime.now())

    database.session.add(notification)

    database.session.commit()

    return {"message": f"Solicitação encaminhada para o helper {helper_refer.NOME}."}, 200

def request_customization_edit(customization_id,
                            nro_tp,
                            making,
                            make,
                            how,
                            benefit,
                            version,
                            docs,
                            user_id,
                            user_type):

    if user_type != "H":
        return {"message": "Você não tem permissão para realizar essa operação."}, 401

    helper = database.session.query(USUARIO).filter(
        USUARIO.ID == user_id).first()

    customization = database.session.query(SOL_CUSTOMIZACAO).filter(
        SOL_CUSTOMIZACAO.id == customization_id).first()

    customization.NRO_TP = nro_tp
    customization.FAZENDO = making
    customization.FAZER = make
    customization.COMO = how
    customization.BENEFICIO = benefit
    customization.VERSAO = version
    customization.DOCS = docs

    mov = MOV_SOL(ID_SOL=customization.id,
                  TIPO_SOL='customization',
                  TITULO="Solicitação editada",
                  TIPO="H",
                  HELPER=helper.NOME,
                  ANALISTA="",
                  RESUMO="Solicitação ajustada.",
                  STATUS="AJUSTE DE INFORMAÇÃO",
                  DTA_CREATE=datetime.now())

    database.session.add(mov)

    notification = NOTIFICACAO(TIPO="Solicitação",
                                 SUBTIPO="Customização",
                                 MENSAGEM=f"Sua solicitação de customização para a TP {customization.NRO_TP} teve uma interação.",
                                 USUARIO_ID=customization.ANALISTA_ID,
                                 DTA_CREATE=datetime.now())

    database.session.add(notification)

    database.session.commit()

    return {"message": "Solicitação alterada."}, 200

def request_customization_list(customization_id, user_id, user_type):
    result = []
    if customization_id == 'undefined':
        if user_type == "A":
            requests_customization = database.session.query(SOL_CUSTOMIZACAO).filter(SOL_CUSTOMIZACAO.ANALISTA_ID==user_id).all()
        elif user_type == "H":
            requests_customization = database.session.query(SOL_CUSTOMIZACAO).filter(SOL_CUSTOMIZACAO.HELPER_ID==user_id).all()
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

            requests_customization = database.session.query(SOL_CUSTOMIZACAO).filter(
                SOL_CUSTOMIZACAO.ANALISTA_ID.in_(list_analyst)).all()
        else:
            requests_customization = database.session.query(SOL_CUSTOMIZACAO).all()

        for customization in requests_customization[::-1]:
            analyst = database.session.query(USUARIO).filter(
                USUARIO.ID == customization.ANALISTA_ID).first()
            helper = database.session.query(USUARIO).filter(
                USUARIO.ID == customization.HELPER_ID).first()

            if customization.DTA_CONCLUDED:
                date_concluded = customization.DTA_CONCLUDED.strftime("%d/%m/%Y %H:%M:%S")
            else:
                date_concluded = customization.DTA_CONCLUDED

            result.append({
                "idcustomization": customization.id,
                "nroTP": customization.NRO_TP,
                "issue": customization.ISSUE,
                "making": customization.FAZENDO,
                "make": customization.FAZER,
                "how": customization.COMO,
                "benefit": customization.BENEFICIO,
                "version": customization.VERSAO,
                "docs": customization.DOCS,
                "solution": customization.SOLUCAO,
                "status": customization.STATUS,
                "helperID": customization.HELPER_ID,
                "helperName": helper.NOME,
                "analystID": customization.ANALISTA_ID,
                "analystName": analyst.NOME,
                "dtaCreate": customization.DTA_CREATE,
                "dtaConcluded": date_concluded
            })
    else:
        customization = database.session.query(SOL_CUSTOMIZACAO).filter(SOL_CUSTOMIZACAO.id == customization_id).first()

        analyst = database.session.query(USUARIO).filter(USUARIO.ID == customization.ANALISTA_ID).first()
        helper = database.session.query(USUARIO).filter(USUARIO.ID == customization.HELPER_ID).first()

        if customization.DTA_CONCLUDED:
            date_concluded = customization.DTA_CONCLUDED.strftime("%d/%m/%Y %H:%M:%S")
        else:
            date_concluded = customization.DTA_CONCLUDED

        result.append({
                "idcustomization": customization.id,
                "nroTP": customization.NRO_TP,
                "issue": customization.ISSUE,
                "making": customization.FAZENDO,
                "make": customization.FAZER,
                "how": customization.COMO,
                "benefit": customization.BENEFICIO,
                "version": customization.VERSAO,
                "docs": customization.DOCS,
                "solution": customization.SOLUCAO,
                "status": customization.STATUS,
                "helperID": customization.HELPER_ID,
                "helperName": helper.NOME,
                "analystID": customization.ANALISTA_ID,
                "analystName": analyst.NOME,
                "dtaCreate": customization.DTA_CREATE,
                "dtaConcluded": date_concluded
            })


    return result

def request_customization_list_all():
    requests_customization = database.session.query(SOL_CUSTOMIZACAO).all()

    result = []

    for customization in requests_customization[::-1]:
        analyst = database.session.query(USUARIO).filter(
            USUARIO.ID == customization.ANALISTA_ID).first()
        helper = database.session.query(USUARIO).filter(
            USUARIO.ID == customization.HELPER_ID).first()

        if customization.DTA_CONCLUDED:
            date_concluded = customization.DTA_CONCLUDED.strftime("%d/%m/%Y %H:%M:%S")
        else:
            date_concluded = customization.DTA_CONCLUDED

        result.append({
            "idcustomization": customization.id,
            "nroTP": customization.NRO_TP,
            "issue": customization.ISSUE,
            "making": customization.FAZENDO,
            "make": customization.FAZER,
            "how": customization.COMO,
            "benefit": customization.BENEFICIO,
            "version": customization.VERSAO,
            "docs": customization.DOCS,
            "solution": customization.SOLUCAO,
            "status": customization.STATUS,
            "helperID": customization.HELPER_ID,
            "helperName": helper.NOME,
            "analystID": customization.ANALISTA_ID,
            "analystName": analyst.NOME,
            "dtaCreate": customization.DTA_CREATE.strftime("%d/%m/%Y %H:%M:%S"),
            "dtaConcluded": date_concluded
        })

    return result
