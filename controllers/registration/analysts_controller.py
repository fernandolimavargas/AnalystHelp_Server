from models.models import *

from extensions.database import database
from extensions.bcrypt import bcrypt


def registration_analyst(name, email, password, office, goal, team_id, user_type):
    if user_type not in ("H", "G", "C"):
        return {"message": "Você não tem permissão para realizar essa operação."}, 401

    analista = database.session.query(ANALISTA).filter(ANALISTA.EMAIL==email).first()

    if analista: 
        return {"message": "Já existe um cadastro para esse e-mail"}, 406

    analista = ANALISTA(USUARIO=name, 
        EMAIL=email, 
        SENHA=bcrypt.generate_password_hash(password),
        META=goal,
        CARGO=office,
        TIME_ID=team_id)

    database.session.add(analista)

    database.session.commit()

    return {"message": "Cadastro realizado com sucesso."}, 200

def edit_analyst(analyst_id, name, email, password, office, goal, team_id, user_email, user_type):
    if (user_type in ("H", "G", "C")) or (user_email == email):
        valid_email = database.session.query(ANALISTA).filter(ANALISTA.id!=analyst_id, ANALISTA.EMAIL==email).first()
        if valid_email:
            return {"message": "Esse email já esta em uso, caso necessario pode ser feita a alteração do mesmo."}, 406

        analista = database.session.query(ANALISTA).filter(ANALISTA.id==analyst_id).first()

        analista.USUARIO=name
        analista.EMAIL=email
        analista.META=goal
        analista.CARGO=office
        analista.TIME_ID=team_id

        database.session.commit()

        return {"message": "Cadastro alterado com sucesso."}, 200   
    
    
    return {"message": "Você não tem permissão para realizar essa operação."}, 401



def delete_analyst(analyst_id, user_type):
    if user_type not in ("H", "G", "C"):
        return {"message": "Você não tem permissão para realizar essa operação."}, 401

    analista = database.session.query(ANALISTA).filter(ANALISTA.id==analyst_id).first()

    request = ((database.session.query(SOL_ERRO).filter(SOL_ERRO.ANALISTA_ID==analista.id).first()
        or database.session.query(SOL_ALTERACAO).filter(SOL_ALTERACAO.ANALISTA_ID==analista.id).first()
        or database.session.query(SOL_CUSTOMIZACAO).filter(SOL_CUSTOMIZACAO.ANALISTA_ID==analista.id).first()
        or database.session.query(SOL_SCRIPT).filter(SOL_SCRIPT.ANALISTA_ID==analista.id).first()
        or database.session.query(SOL_SERVICO).filter(SOL_SERVICO.ANALISTA_ID==analista.id).first()
        or database.session.query(SOL_IMPORT).filter(SOL_IMPORT.ANALISTA_ID==analista.id).first()
        or database.session.query(SOL_SHARE).filter(SOL_SHARE.ANALISTA_ID==analista.id).first()
        or database.session.query(SOL_TICKET).filter(SOL_TICKET.ANALISTA_ID==analista.id).first()
        or database.session.query(SOL_ISSUE_INT).filter(SOL_ISSUE_INT.ANALISTA_ID==analista.id).first()
        or database.session.query(HELP).filter(HELP.ANALISTA_ID==analista.id).first()))

    if request:
        return {"message": "Esse cadastro possui solicitações vinculadas, faça a inativação do mesmo caso necessario."}, 406


    database.session.delete(analista)

    database.session.commit()

    return {"message": "Cadastro excluido com sucesso."}, 200

def list_analyst(user_type):
    if user_type not in ("H", "G", "C"):
        return {"message": "Você não tem permissão para realizar essa operação."}, 401

    analistas = database.session.query(ANALISTA).order_by(ANALISTA.USUARIO).all()

    result = []

    for analista in analistas:
        result.append({
            "id": analista.id,
            "name": analista.USUARIO,
            "email": analista.EMAIL,
            "office": analista.CARGO,
            "goal": analista.META,
            "team": analista.TIME_ID
        })

    return result