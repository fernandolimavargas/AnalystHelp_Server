from models.models import *

from extensions.database import database
from extensions.bcrypt import bcrypt


def user_registration(
    name,
    email,
    password,
    user_type_reg,
    goal,
    office,
    committee,
    inactive,
    team_id, 
    user_type):

    if user_type_reg in ("A", "H") and user_type not in ("H", "G", "C"):
        return {"message": "Você não tem permissão para realizar essa operação."}, 401
    elif user_type_reg == "G" and user_type not in ("G", "C"):
        return {"message": "Você não tem permissão para realizar essa operação."}, 401
    elif user_type_reg == "C" and user_type not in ("C"):
        return {"message": "Você não tem permissão para realizar essa operação."}, 401

    user = database.session.query(USUARIO).filter(
        USUARIO.EMAIL == email).first()

    if user:
        return {"message": "Já existe um cadastro para esse e-mail"}, 406

    user = USUARIO(NOME=name,
                EMAIL=email,
                SENHA=bcrypt.generate_password_hash(password),
                TIPO=user_type_reg,
                META=goal,
                CARGO=office,
                COMITE=committee,
                INATIVO=inactive,
                TIME_ID=team_id)

    database.session.add(user)

    database.session.commit()

    return {"message": "Cadastro realizado com sucesso."}, 200


def user_alteration(user_id,
    name,
    email,
    password,
    user_type_reg,
    goal,
    office,
    committee,
    inactive,
    team_id, 
    user_email, 
    user_type):

    if (user_type_reg == "A" and user_type not in ("H", "G", "C")) and (user_email != email):
        return {"message": "Você não tem permissão para realizar essa operação."}, 401         
    elif (user_type_reg == "H" and user_type not in ("G", "C")) and (user_email != email):
        return {"message": "Você não tem permissão para realizar essa operação."}, 401
    elif user_type_reg in "G" and user_type != "C" and (user_email != email):
        return {"message": "Você não tem permissão para realizar essa operação."}, 401
    elif user_type_reg == "C" and user_type != "C":
        return {"message": "Você não tem permissão para realizar essa operação."}, 401

    valid_email = database.session.query(USUARIO).filter(
        USUARIO.ID != user_id, USUARIO.EMAIL == email).first()

    if valid_email:
        return {"message": "Esse email já esta em uso, caso necessario pode ser feita a alteração do mesmo."}, 406

    user = database.session.query(USUARIO).filter(
        USUARIO.ID == user_id).first()

    user.NOME = name
    user.EMAIL = email
    if password:
        user.SENHA = bcrypt.generate_password_hash(password)
    user.TIPO = user_type_reg
    user.META = goal
    user.CARGO = office
    user.COMITE = committee
    user.INATIVO = inactive
    user.TIME_ID = team_id

    database.session.commit()

    return {"message": "Cadastro alterado com sucesso."}, 200

def user_delete(user_id, user_type_reg, user_type):
    if (user_type_reg == "A" and user_type not in ("H", "G", "C")):
        return {"message": "Você não tem permissão para realizar essa operação."}, 401         
    elif (user_type_reg == "H" and user_type not in ("G", "C")):
        return {"message": "Você não tem permissão para realizar essa operação."}, 401
    elif user_type_reg in "G" and user_type != "C":
        return {"message": "Você não tem permissão para realizar essa operação."}, 401
    elif user_type_reg == "C" and user_type != "C":
        return {"message": "Você não tem permissão para realizar essa operação."}, 401

    user = database.session.query(USUARIO).filter(
        USUARIO.ID == user_id).first()
    
    occurrences = database.session.query(OCORRENCIA).filter(OCORRENCIA.ANALISTA_ID==user.ID).first()

    if occurrences:
        return {"message": "Esse cadastro possui ocorrencias vinculadas a ele, faça a exclusão e após isso tente novamente."}, 406

    request = ((database.session.query(SOL_ERRO).filter(SOL_ERRO.ANALISTA_ID == user.ID).first()
                or database.session.query(SOL_ALTERACAO).filter(SOL_ALTERACAO.ANALISTA_ID == user.ID).first()
                or database.session.query(SOL_CUSTOMIZACAO).filter(SOL_CUSTOMIZACAO.ANALISTA_ID == user.ID).first()
                or database.session.query(SOL_SCRIPT).filter(SOL_SCRIPT.ANALISTA_ID == user.ID).first()
                or database.session.query(SOL_SERVICO).filter(SOL_SERVICO.ANALISTA_ID == user.ID).first()
                or database.session.query(SOL_IMPORT).filter(SOL_IMPORT.ANALISTA_ID == user.ID).first()
                or database.session.query(SOL_SHARE).filter(SOL_SHARE.ANALISTA_ID == user.ID).first()
                or database.session.query(SOL_TICKET).filter(SOL_TICKET.ANALISTA_ID == user.ID).first()
                or database.session.query(SOL_ISSUE_INT).filter(SOL_ISSUE_INT.ANALISTA_ID == user.ID).first()
                or database.session.query(HELP).filter(HELP.ANALISTA_ID == user.ID).first()))

    if request:
        return {"message": "Esse cadastro possui solicitações vinculadas, faça a inativação do mesmo caso necessario."}, 406

    database.session.delete(user)

    database.session.commit()

    return {"message": "Cadastro excluido com sucesso."}, 200


def user_listing(user_profile, user_id, user_type):
    result = []

    if user_profile != 'undefined' and user_type == "A":
        user = database.session.query(USUARIO).filter(USUARIO.ID == user_id).first()
        time = database.session.query(TIME).filter(TIME.id == user.TIME_ID).first()
        helper = database.session.query(USUARIO).filter(USUARIO.ID == time.HELPER_ID).first()
        gestor = database.session.query(USUARIO).filter(USUARIO.ID == time.GESTOR_ID).first()

        result.append({
            "id": user.ID,
            "name": user.NOME,
            "email": user.EMAIL,
            "type": user.TIPO,
            "goal": user.META,
            "office": user.CARGO,
            "committee": user.COMITE,
            "inactive": user.INATIVO,
            "team": user.TIME_ID,
            "helper": helper.NOME,
            "gestor": gestor.NOME
        })

    elif user_profile != 'undefined' and user_type == "H":
        user = database.session.query(USUARIO).filter(USUARIO.ID == user_id).first()
        time = database.session.query(TIME).filter(TIME.HELPER_ID == user_id).first()
        gestor = database.session.query(USUARIO).filter(USUARIO.ID == time.GESTOR_ID).first()

        result.append({
            "id": user.ID,
            "name": user.NOME,
            "email": user.EMAIL,
            "type": user.TIPO,
            "goal": user.META,
            "office": user.CARGO,
            "committee": user.COMITE,
            "inactive": user.INATIVO,
            "team": user.TIME_ID,
            "gestor": gestor.NOME
        })
    elif user_profile != 'undefined' and user_type in ("G", "C"):
        user = database.session.query(USUARIO).filter(USUARIO.ID == user_id).first()

        result.append({
            "id": user.ID,
            "name": user.NOME,
            "email": user.EMAIL,
            "type": user.TIPO,
            "goal": user.META,
            "office": user.CARGO,
            "committee": user.COMITE,
            "team": user.TIME_ID,
            "inactive": user.INATIVO
        })   
    else:
        if user_type not in ("H", "G", "C"):
            return {"message": "Você não tem permissão para realizar essa operação."}, 401

        users = database.session.query(
            USUARIO).order_by(USUARIO.NOME).all()

        for user in users:
            result.append({
                "id": user.ID,
                "name": user.NOME,
                "email": user.EMAIL,
                "type": user.TIPO,
                "goal": user.META,
                "office": user.CARGO,
                "committee": user.COMITE,
                "inactive": user.INATIVO,
                "team": user.TIME_ID
            })

    return result
