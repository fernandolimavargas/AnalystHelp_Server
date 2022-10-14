from models.models import  *

from extensions.database import database
from extensions.bcrypt import bcrypt


def registration_helper(name, email, password, user_type):
    if user_type not in ("G", "C"):
        return {"message": "Você não tem permissão para realizar essa operação."}, 401

    helper = database.session.query(HELPER).filter(HELPER.EMAIL==email).first()

    if helper: 
        return {"message": "Já existe um cadastro para esse e-mail"}, 406

    helper = HELPER(USUARIO=name, EMAIL=email, SENHA=bcrypt.generate_password_hash(password))

    database.session.add(helper)
    database.session.commit()

    return {"message": "Cadastro realizado com sucesso."}, 200

def edit_helper(helper_id, name, email, password, user_email, user_type):
    if (user_type in ("G", "C")) or (user_email == email):
        valid_email = database.session.query(HELPER).filter(HELPER.id!=helper_id, HELPER.EMAIL==email).first()
        if valid_email:
            return {"message": "Esse email já esta em uso, caso necessario pode ser feita a alteração do mesmo."}, 406

        helper = database.session.query(HELPER).filter(HELPER.id==helper_id).first()

        helper.USUARIO=name
        helper.EMAIL=email
        helper.SENHA=bcrypt.generate_password_hash(password)

        database.session.commit()

        return {"message": "Cadastro alterado com sucesso."}, 200

    return {"message": "Você não tem permissão para realizar essa operação."}, 401


def delete_helper(helper_id, user_type):
    if user_type not in ("G", "C"):
        return {"message": "Você não tem permissão para realizar essa operação."}, 401

    helper = database.session.query(HELPER).filter(HELPER.id==helper_id).first()
    time = database.session.query(TIME).filter(TIME.HELPER_ID==helper.id).first()

    if time: 
        return {"message": f"Esse helper está vinculado ao time {time.NOME}, desvincule-o para excluir esse helper."}, 406

    request = ((database.session.query(SOL_ERRO).filter(SOL_ERRO.HELPER_ID==helper.id).first()
        or database.session.query(SOL_ALTERACAO).filter(SOL_ALTERACAO.HELPER_ID==helper.id).first()
        or database.session.query(SOL_CUSTOMIZACAO).filter(SOL_CUSTOMIZACAO.HELPER_ID==helper.id).first()
        or database.session.query(SOL_SCRIPT).filter(SOL_SCRIPT.HELPER_ID==helper.id).first()
        or database.session.query(SOL_SERVICO).filter(SOL_SERVICO.HELPER_ID==helper.id).first()
        or database.session.query(SOL_IMPORT).filter(SOL_IMPORT.HELPER_ID==helper.id).first()
        or database.session.query(SOL_SHARE).filter(SOL_SHARE.HELPER_ID==helper.id).first()
        or database.session.query(SOL_TICKET).filter(SOL_TICKET.HELPER_ID==helper.id).first()
        or database.session.query(SOL_ISSUE_INT).filter(SOL_ISSUE_INT.HELPER_ID==helper.id).first()
        or database.session.query(HELP).filter(HELP.HELPER_ID==helper.id).first()))

    if request:
        return {"message": "Esse cadastro possui solicitações vinculadas, faça a inativação do mesmo caso necessario."}, 406

    database.session.delete(helper)
    database.session.commit()

    return {"message": "Cadastro excluido com sucesso."}, 200



def list_helper(user_type):
    if user_type not in ("H", "G", "C"):
        return {"message": "Você não tem permissão para realizar essa operação."}, 401

    helpers = database.session.query(HELPER).order_by(HELPER.USUARIO).all()

    result = []

    for helper in helpers:
        result.append({
            "id": helper.id,
            "name": helper.USUARIO,
            "email": helper.EMAIL,
        })

    return result