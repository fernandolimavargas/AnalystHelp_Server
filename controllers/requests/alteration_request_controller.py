from extensions.database import database
from models.models import USUARIO, SOL_ALTERACAO, TIME, MOV_SOL, NOTIFICACAO
from datetime import datetime

def request_alteration(nro_tp, 
                        making, 
                        make, 
                        how, 
                        benefit, 
                        version, 
                        docs, 
                        analyst_id, 
                        duplicate):
    alteration = database.session.query(SOL_ALTERACAO).filter(SOL_ALTERACAO.NRO_TP == nro_tp)

    if alteration and not duplicate:
        return {"message": "Já existe uma solicitação de alteração para essa TP!"}, 406
    
    analyst = database.session.query(USUARIO).filter(
        USUARIO.ID == analyst_id).first()
    group = database.session.query(TIME).filter(
        TIME.id == analyst.TIME_ID).first()
    helper = database.session.query(USUARIO).filter(
        USUARIO.ID == group.HELPER_ID).first()

    alteration = SOL_ALTERACAO(NRO_TP=nro_tp,
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
    
    database.session.add(alteration)

    database.session.commit()

    alteration = database.session.query(SOL_ALTERACAO).filter(
        SOL_ALTERACAO.NRO_TP == nro_tp).order_by(SOL_ALTERACAO.id.desc()).first()

    mov = MOV_SOL(ID_SOL=alteration.id,
                  TIPO_SOL='alteration',
                  TITULO="Abertura de analise",
                  TIPO="A",
                  HELPER="",
                  ANALISTA=analyst.NOME,
                  RESUMO="Solicitação de alteração aberta.",
                  STATUS="AGUARDANDO INICIALIZAÇÃO",
                  DTA_CREATE=datetime.now())

    database.session.add(mov)

    notification = NOTIFICACAO(TIPO="Solicitação",
                                 SUBTIPO="Alteração",
                                 MENSAGEM=f"Foi aberta uma solicitação de alteração para a TP {nro_tp}.",
                                 USUARIO_ID=helper.ID,
                                 DTA_CREATE=datetime.now())

    database.session.add(notification)

    database.session.commit()


    return {"message": "Solicitação de análise de alteração enviada!"}, 200

def request_alteration_start(alteration_id, user_id, user_type):
    if user_type != "H":
        return {"message": "Você não tem permissão para realizar essa operação."}, 401

    helper = database.session.query(USUARIO).filter(
        USUARIO.ID == user_id).first()
    
    alteration = database.session.query(SOL_ALTERACAO).filter(
        SOL_ALTERACAO.id == alteration_id).first()

    alteration.STATUS = "EM ANALISE"

    mov = MOV_SOL(ID_SOL=alteration.id,
                  TIPO_SOL='alteration',
                  TITULO="Análise iniciada",
                  TIPO="H",
                  HELPER=helper.NOME,
                  ANALISTA="",
                  RESUMO="Sua analise está em andamento.",
                  STATUS="EM ANALISE",
                  DTA_CREATE=datetime.now())

    database.session.add(mov)

    notification = NOTIFICACAO(TIPO="Solicitação",
                                 SUBTIPO="ALTERAÇÃO",
                                 MENSAGEM=f"Sua solicitação de alteração para a TP {alteration.NRO_TP} teve uma interação.",
                                 USUARIO_ID=alteration.ANALISTA_ID,
                                 DTA_CREATE=datetime.now())

    database.session.add(notification)

    database.session.commit()


    return {"message": "Solicitação de análise de alteração iniciada!"}, 200

def request_alteration_information(alteration_id, message, user_id, user_type):
    if user_type != "H":
        return {"message": "Você não tem permissão para realizar essa operação."}, 401
    
    
    helper = database.session.query(USUARIO).filter(
        USUARIO.ID == user_id).first()

    alteration = database.session.query(SOL_ALTERACAO).filter(
        SOL_ALTERACAO.id == alteration_id).first()

    alteration.STATUS = "AGUARDANDO INFORMAÇÃO"

    mov = MOV_SOL(ID_SOL=alteration.id,
                  TIPO_SOL='alteration',
                  TITULO="Solicitação de Informação",
                  TIPO="H",
                  HELPER=helper.NOME,
                  ANALISTA="",
                  RESUMO=message,
                  STATUS="AGUARDANDO INFORMAÇÃO",
                  DTA_CREATE=datetime.now())

    database.session.add(mov)

    notification = NOTIFICACAO(TIPO="Solicitação",
                                 SUBTIPO="Alteração",
                                 MENSAGEM=f"Sua solicitação de alteração para a TP {alteration.NRO_TP} teve uma interação.",
                                 USUARIO_ID=alteration.ANALISTA_ID,
                                 DTA_CREATE=datetime.now())

    database.session.add(notification)

    database.session.commit()

    return {"message": "Solicitação de informação enviada ao analista."}, 200

def request_alteration_information_response(alteration_id,
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
    alteration = database.session.query(SOL_ALTERACAO).filter(
        SOL_ALTERACAO.id == alteration_id).first()

    if alteration.ANALISTA_ID != user_id and user_type != "A":
        return {"message": "Você não tem permissão para realizar essa operação."}, 401

    alteration.NRO_TP = nro_tp
    alteration.FAZENDO = making
    alteration.FAZER = make
    alteration.COMO = how
    alteration.BENEFICIO = benefit
    alteration.VERSION = version
    alteration.DOCS = docs
    alteration.STATUS = "EM ANALISE"

    analyst = database.session.query(USUARIO).filter(
        USUARIO.ID == alteration.ANALISTA_ID).first()

    mov = MOV_SOL(ID_SOL=alteration.id,
                  TIPO_SOL='alteration',
                  TITULO="Solicitação de informação respondida",
                  TIPO="A",
                  HELPER="",
                  ANALISTA=analyst.NOME,
                  RESUMO=message,
                  STATUS="AGUARDANDO INFORMAÇÃO",
                  DTA_CREATE=datetime.now())

    database.session.add(mov)

    notification = NOTIFICACAO(TIPO="Solicitação",
                                 SUBTIPO="Alteração",
                                 MENSAGEM=f"Sua solicitação de alteração para a TP {alteration.NRO_TP} teve uma interação.",
                                 USUARIO_ID=alteration.HELPER_ID,
                                 DTA_CREATE=datetime.now())

    database.session.add(notification)

    database.session.commit()

    return {"message": "Solicitação de informação repondida."}, 200

def request_alteration_aproved(alteration_id, message, user_id, user_type):
    if user_type != "H":
        return {"message": "Você não tem permissão para realizar essa operação."}, 401

    helper = database.session.query(USUARIO).filter(
        USUARIO.ID == user_id).first()

    alteration = database.session.query(SOL_ALTERACAO).filter(
        SOL_ALTERACAO.id == alteration_id).first()

    alteration.SOLUCAO = message
    alteration.STATUS = "ANALISE COMITE"

    mov = MOV_SOL(ID_SOL=alteration.id,
                  TIPO_SOL='alteration',
                  TITULO="Enviada para analise comite",
                  TIPO="H",
                  HELPER=helper.NOME,
                  ANALISTA="",
                  RESUMO="Solicitação foi para aprovação do comite",
                  STATUS="ANALISE COMITE",
                  DTA_CREATE=datetime.now())

    database.session.add(mov)

    notification = NOTIFICACAO(TIPO="Solicitação",
                                 SUBTIPO="Alteração",
                                 MENSAGEM=f"Sua solicitação de alteração para a TP {alteration.NRO_TP} teve uma interação.",
                                 USUARIO_ID=alteration.ANALISTA_ID,
                                 DTA_CREATE=datetime.now())

    database.session.add(notification)

    database.session.commit()

    return {"message": "Solicitação de análise de alteração foi para analise comite."}, 200


def request_alteration_committee_aproved(alteration_id, message, user_id, user_type):
    if user_type != "H":
        return {"message": "Você não tem permissão para realizar essa operação."}, 401

    helper = database.session.query(USUARIO).filter(
        USUARIO.ID == user_id).first()

    alteration = database.session.query(SOL_ALTERACAO).filter(
        SOL_ALTERACAO.id == alteration_id).first()

    alteration.SOLUCAO = message
    alteration.STATUS = "AGUARDANDO ABERTURA DE ISSUE"

    mov = MOV_SOL(ID_SOL=alteration.id,
                  TIPO_SOL='alteration',
                  TITULO="Aprovada abertura de ISSUE",
                  TIPO="H",
                  HELPER=helper.NOME,
                  ANALISTA="",
                  RESUMO="Solicitação aprovada, não se esqueça de validar a taxonomia da TP antes de enviar para alteração.",
                  STATUS="AGUARDANDO ABERTURA DE ISSUE",
                  DTA_CREATE=datetime.now())

    database.session.add(mov)

    notification = NOTIFICACAO(TIPO="Solicitação",
                                 SUBTIPO="Alteração",
                                 MENSAGEM=f"Sua solicitação de alteração para a TP {alteration.NRO_TP} teve uma interação.",
                                 USUARIO_ID=alteration.ANALISTA_ID,
                                 DTA_CREATE=datetime.now())

    database.session.add(notification)

    database.session.commit()

    return {"message": "Solicitação de análise de alteração aprovada."}, 200

def request_alteration_mark(alteration_id, issue, user_id, user_type):
    alteration = database.session.query(SOL_ALTERACAO).filter(SOL_ALTERACAO.id == alteration_id).first()

    if alteration.ANALISTA_ID != user_id and user_type != "A":
        return {"message": "Você não tem permissão para realizar essa operação."}, 401

    analyst = USUARIO.query.filter_by(ID=alteration.ANALISTA_ID).first()

    alteration.ISSUE = issue
    alteration.STATUS = "AGUARDANDO ADIÇÃO DE RÓTULO"

    mov = MOV_SOL(ID_SOL=alteration.id,
                  TIPO_SOL='alteration',
                  TITULO="Solicitação de rótulo no JIRA",
                  TIPO="A",
                  HELPER="",
                  ANALISTA=analyst.NOME,
                  RESUMO="ISSUE aberta e informada na solicitação favor adicionar o rótulo.",
                  STATUS="AGUARDANDO ADIÇÃO DE RÓTULO",
                  DTA_CREATE=datetime.now())

    database.session.add(mov)

    notification = NOTIFICACAO(TIPO="Solicitação",
                                 SUBTIPO="Alteração",
                                 MENSAGEM=f"Sua solicitação de alteração para a TP {alteration.NRO_TP} teve uma interação.",
                                 USUARIO_ID=alteration.HELPER_ID,
                                 DTA_CREATE=datetime.now())

    database.session.add(notification)

    database.session.commit()

    return {"message": "Solicitação de adição de rótulo enviada ao comite"}, 200

def request_alteration_finished(alteration_id, message, user_id, user_type):
    if user_type != "H":
        return {"message": "Você não tem permissão para realizar essa operação."}, 401

    helper = database.session.query(USUARIO).filter(
        USUARIO.ID == user_id).first()

    alteration = database.session.query(SOL_ALTERACAO).filter(
        SOL_ALTERACAO.id == alteration_id).first()

    alteration.SOLUCAO = message
    alteration.STATUS = "FINALIZADA"
    alteration.DTA_CONCLUDED = datetime.now()

    mov = MOV_SOL(ID_SOL=alteration.id,
                  TIPO_SOL='alteration',
                  TITULO="Solicitação de rótulo no JIRA",
                  TIPO="H",
                  HELPER=helper.NOME,
                  ANALISTA="",
                  RESUMO="Rótulo adicionado.",
                  STATUS="FINALIZADA",
                  DTA_CREATE=datetime.now())

    database.session.add(mov)

    notification = NOTIFICACAO(TIPO="Solicitação",
                                 SUBTIPO="Erro",
                                 MENSAGEM=f"Sua solicitação de alteração para a TP {alteration.NRO_TP} teve uma interação.",
                                 USUARIO_ID=alteration.ANALISTA_ID,
                                 DTA_CREATE=datetime.now())

    database.session.add(notification)

    database.session.commit()

    return {"message": "Solicitação finalizada."}, 200

def request_alteration_recused(alteration_id, message, user_id, user_type):
    if user_type != "H":
        return {"message": "Você não tem permissão para realizar essa operação."}, 401

    helper = database.session.query(USUARIO).filter(
        USUARIO.ID == user_id).first()

    alteration = database.session.query(SOL_ALTERACAO).filter(
        SOL_ALTERACAO.id == alteration_id).first()

    alteration.SOLUCAO = message
    alteration.STATUS = "NÃO APROVADO"
    alteration.DTA_CONCLUDED = datetime.now()

    mov = MOV_SOL(ID_SOL=alteration.id,
                  TIPO_SOL='alteration',
                  TITULO="Solicitação recusada",
                  TIPO="H",
                  HELPER=helper.NOME,
                  ANALISTA="",
                  RESUMO="Solicitação não aprovada.",
                  STATUS="NÃO APROVADO",
                  DTA_CREATE=datetime.now())

    database.session.add(mov)

    notification = NOTIFICACAO(TIPO="Solicitação",
                                 SUBTIPO="Alteração",
                                 MENSAGEM=f"Sua solicitação de alteração para a TP {alteration.NRO_TP} teve uma interação.",
                                 USUARIO_ID=alteration.ANALISTA_ID,
                                 DTA_CREATE=datetime.now())

    database.session.add(notification)

    database.session.commit()

    return {"message": "Solicitação recusada."}, 200

def request_alteration_committee_recused(alteration_id, message, user_id, user_type):
    if user_type != "H":
        return {"message": "Você não tem permissão para realizar essa operação."}, 401

    helper = database.session.query(USUARIO).filter(
        USUARIO.ID == user_id).first()

    alteration = database.session.query(SOL_ALTERACAO).filter(
        SOL_ALTERACAO.id == alteration_id).first()

    alteration.SOLUCAO = message
    alteration.STATUS = "NÃO APROVADO COMITE"
    alteration.DTA_CONCLUDED = datetime.now()

    mov = MOV_SOL(ID_SOL=alteration.id,
                  TIPO_SOL='alteration',
                  TITULO="Solicitação recusada",
                  TIPO="H",
                  HELPER=helper.NOME,
                  ANALISTA="",
                  RESUMO="Solicitação não aprovada.",
                  STATUS="NÃO APROVADO COMITE",
                  DTA_CREATE=datetime.now())

    database.session.add(mov)

    notification = NOTIFICACAO(TIPO="Solicitação",
                                 SUBTIPO="Alteração",
                                 MENSAGEM=f"Sua solicitação de alteração para a TP {alteration.NRO_TP} teve uma interação.",
                                 USUARIO_ID=alteration.ANALISTA_ID,
                                 DTA_CREATE=datetime.now())

    database.session.add(notification)

    database.session.commit()

    return {"message": "Solicitação recusada."}, 200

def request_alteration_refer(alteration_id, helper_to_forward, user_id, user_type):
    if user_type != "H":
        return {"message": "Você não tem permissão para realizar essa operação."}, 401

    helper = database.session.query(USUARIO).filter(
        USUARIO.ID == user_id).first()

    alteration = database.session.query(SOL_ALTERACAO).filter(
        SOL_ALTERACAO.id == alteration_id).first()

    helper_refer = database.session.query(USUARIO).filter(
        USUARIO.ID == helper_to_forward).first()

    alteration.HELPER_ID = helper_to_forward
    alteration.STATUS = "NÃO INICIADO"

    mov = MOV_SOL(ID_SOL=alteration.id,
                  TIPO_SOL='alteration',
                  TITULO="Solicitação encaminhada",
                  TIPO="H",
                  HELPER=helper.NOME,
                  ANALISTA="",
                  RESUMO="Solicitação encaminhada.",
                  STATUS="NÃO INICIADO",
                  DTA_CREATE=datetime.now())

    database.session.add(mov)

    notification = NOTIFICACAO(TIPO="Solicitação",
                                 SUBTIPO="Alteração",
                                 MENSAGEM=f"Sua solicitação de alteração para a TP {alteration.NRO_TP} teve uma interação.",
                                 USUARIO_ID=alteration.ANALISTA_ID,
                                 DTA_CREATE=datetime.now())

    database.session.add(notification)

    notification = NOTIFICACAO(TIPO="Solicitação",
                                 SUBTIPO="Alteração",
                                 MENSAGEM=f"Foi encaminhada uma solicitação de alteração para a TP {alteration.NRO_TP}.",
                                 USUARIO_ID=helper_to_forward,
                                 DTA_CREATE=datetime.now())

    database.session.add(notification)

    database.session.commit()

    return {"message": f"Solicitação encaminhada para o helper {helper_refer.NOME}."}, 200

def request_alteration_edit(alteration_id,
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

    alteration = database.session.query(SOL_ALTERACAO).filter(
        SOL_ALTERACAO.id == alteration_id).first()

    alteration.NRO_TP = nro_tp
    alteration.FAZENDO = making
    alteration.FAZER = make
    alteration.COMO = how
    alteration.BENEFICIO = benefit
    alteration.VERSAO = version
    alteration.DOCS = docs

    mov = MOV_SOL(ID_SOL=alteration.id,
                  TIPO_SOL='alteration',
                  TITULO="Solicitação editada",
                  TIPO="H",
                  HELPER=helper.NOME,
                  ANALISTA="",
                  RESUMO="Solicitação ajustada.",
                  STATUS="AJUSTE DE INFORMAÇÃO",
                  DTA_CREATE=datetime.now())

    database.session.add(mov)

    notification = NOTIFICACAO(TIPO="Solicitação",
                                 SUBTIPO="Alteração",
                                 MENSAGEM=f"Sua solicitação de alteração para a TP {alteration.NRO_TP} teve uma interação.",
                                 USUARIO_ID=alteration.ANALISTA_ID,
                                 DTA_CREATE=datetime.now())

    database.session.add(notification)

    database.session.commit()

    return {"message": "Solicitação alterada."}, 200

def request_alteration_list(alteration_id, user_id, user_type):
    result = []
    if alteration_id == 'undefined':
        if user_type == "A":
            requests_alteration = database.session.query(SOL_ALTERACAO).filter(SOL_ALTERACAO.ANALISTA_ID==user_id).all()
        elif user_type == "H":
            requests_alteration = database.session.query(SOL_ALTERACAO).filter(SOL_ALTERACAO.HELPER_ID==user_id).all()
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

            requests_alteration = database.session.query(SOL_ALTERACAO).filter(
                SOL_ALTERACAO.ANALISTA_ID.in_(list_analyst)).all()
        else:
            requests_alteration = database.session.query(SOL_ALTERACAO).all()

        for alteration in requests_alteration[::-1]:
            analyst = database.session.query(USUARIO).filter(
                USUARIO.ID == alteration.ANALISTA_ID).first()
            helper = database.session.query(USUARIO).filter(
                USUARIO.ID == alteration.HELPER_ID).first()
            
            if alteration.DTA_CONCLUDED:
                date_concluded = alteration.DTA_CONCLUDED.strftime("%d/%m/%Y %H:%M:%S")
            else:
                date_concluded = alteration.DTA_CONCLUDED

            result.append({
                "idAlteration": alteration.id,
                "nroTP": alteration.NRO_TP,
                "issue": alteration.ISSUE,
                "making": alteration.FAZENDO,
                "make": alteration.FAZER,
                "how": alteration.COMO,
                "benefit": alteration.BENEFICIO,
                "version": alteration.VERSAO,
                "docs": alteration.DOCS,
                "solution": alteration.SOLUCAO,
                "status": alteration.STATUS,
                "helperID": alteration.HELPER_ID,
                "helperName": helper.NOME,
                "analystID": alteration.ANALISTA_ID,
                "analystName": analyst.NOME,
                "dtaCreate": alteration.DTA_CREATE.strftime("%d/%m/%Y %H:%M:%S"),
                "dtaConcluded": date_concluded
            })
    else: 
        alteration = database.session.query(SOL_ALTERACAO).filter(SOL_ALTERACAO.id == alteration_id).first()

        analyst = database.session.query(USUARIO).filter(USUARIO.ID == alteration.ANALISTA_ID).first()
        helper = database.session.query(USUARIO).filter(USUARIO.ID == alteration.HELPER_ID).first()

        if alteration.DTA_CONCLUDED:
            date_concluded = alteration.DTA_CONCLUDED.strftime("%d/%m/%Y %H:%M:%S")
        else:
            date_concluded = alteration.DTA_CONCLUDED
        
        result.append({
                "idAlteration": alteration.id,
                "nroTP": alteration.NRO_TP,
                "issue": alteration.ISSUE,
                "making": alteration.FAZENDO,
                "make": alteration.FAZER,
                "how": alteration.COMO,
                "benefit": alteration.BENEFICIO,
                "version": alteration.VERSAO,
                "docs": alteration.DOCS,
                "solution": alteration.SOLUCAO,
                "status": alteration.STATUS,
                "helperID": alteration.HELPER_ID,
                "helperName": helper.NOME,
                "analystID": alteration.ANALISTA_ID,
                "analystName": analyst.NOME,
                "dtaCreate": alteration.DTA_CREATE.strftime("%d/%m/%Y %H:%M:%S"),
                "dtaConcluded": date_concluded
            })

    return result

def request_alteration_list_all():
    requests_alteration = database.session.query(SOL_ALTERACAO).all()

    result = []

    for alteration in requests_alteration[::-1]:
        analyst = database.session.query(USUARIO).filter(
            USUARIO.ID == alteration.ANALISTA_ID).first()
        helper = database.session.query(USUARIO).filter(
            USUARIO.ID == alteration.HELPER_ID).first()

        if alteration.DTA_CONCLUDED:
            date_concluded = alteration.DTA_CONCLUDED.strftime("%d/%m/%Y %H:%M:%S")
        else:
            date_concluded = alteration.DTA_CONCLUDED

        result.append({
            "idAlteration": alteration.id,
            "nroTP": alteration.NRO_TP,
            "issue": alteration.ISSUE,
            "making": alteration.FAZENDO,
            "make": alteration.FAZER,
            "how": alteration.COMO,
            "benefit": alteration.BENEFICIO,
            "version": alteration.VERSAO,
            "docs": alteration.DOCS,
            "solution": alteration.SOLUCAO,
            "status": alteration.STATUS,
            "helperID": alteration.HELPER_ID,
            "helperName": helper.NOME,
            "analystID": alteration.ANALISTA_ID,
            "analystName": analyst.NOME,
            "dtaCreate": alteration.DTA_CREATE.strftime("%d/%m/%Y %H:%M:%S"),
            "dtaConcluded": date_concluded
        })

    return result
