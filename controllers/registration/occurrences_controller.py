from models.models import GESTOR, OCORRENCIA

from extensions.database import database


def registration_occurrences(analyst_id, note, oc_type, dta_start, dta_end, user_type):
    if user_type not in ("G", "C"):
        return {"message": "Você não tem permissão para realizar essa operação."}, 401


    occurrence = database.session.query(OCORRENCIA).filter(
        OCORRENCIA.DTA_INICIO>=dta_start, 
        OCORRENCIA.DTA_FIM<=dta_end, 
        OCORRENCIA.ANALISTA_ID==analyst_id).first()

    if occurrence:
        return {"message": "Já existe uma ocorrencia que engloba essa solicitação."}, 406


    occurrence = OCORRENCIA(ANALISTA_ID=analyst_id, OBSERVACAO=note, TIPO=oc_type, DTA_INICIO=dta_start, DTA_FIM=dta_end)

    database.session.add(occurrence)

    database.session.commit()
    
    return {"message": "Registro realizado com sucesso."}, 200

def edit_occurrences(occurrence_id, analyst_id, note, oc_type, dta_start, dta_end, user_type):
    if user_type not in ("G", "C"):
        return {"message": "Você não tem permissão para realizar essa operação."}, 401

    occurrence = database.session.query(OCORRENCIA).filter(
        OCORRENCIA.id!=occurrence_id,
        OCORRENCIA.DTA_INICIO>=dta_start, 
        OCORRENCIA.DTA_FIM<=dta_end, 
        OCORRENCIA.ANALISTA_ID==analyst_id).first()

    if occurrence:
        return {"message": "Já existe uma ocorrencia que engloba essa solicitação."}, 406

    occurrence = database.session.query(OCORRENCIA).filter(OCORRENCIA.id==occurrence_id).first()

    occurrence.OBSERVACAO = note
    occurrence.TIPO = oc_type
    occurrence.DTA_INICIO = dta_start
    occurrence.DTA_FIM = dta_end

    database.session.commit()
        
    return {"message": "Registro alterado com sucesso."}, 200


def delete_occurrences(occurrence_id, user_type):
    if user_type not in ("G", "C"):
        return {"message": "Você não tem permissão para realizar essa operação."}, 401

    occurrence = database.session.query(OCORRENCIA).filter(OCORRENCIA.id==occurrence_id).first()

    database.session.delete(occurrence)
    database.session.commit()

    return {"message": "Registro excluido com sucesso."}, 200

def list_occurrences(analyst_id, user_type):
    if user_type not in ("H", "G", "C"):
        return {"message": "Você não tem permissão para realizar essa operação."}, 401

    occurrences = database.session.query(OCORRENCIA).filter(OCORRENCIA.ANALISTA_ID==analyst_id).all()

    result = []

    for occurence in occurrences:
        result.append({
            "id": occurence.id,
            "analystID": occurence.ANALISTA_ID,
            "note": occurence.OBSERVACAO,
            "dtaStart": occurence.DTA_INICIO.strftime("%Y-%d-%m"),
            "dtaEnd": occurence.DTA_FIM.strftime("%Y-%d-%m")
        })

    return result