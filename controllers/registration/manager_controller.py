from models.models import GESTOR, TIME

from extensions.database import database
from extensions.bcrypt import bcrypt

def registration_manager(name, email, password, user_type):
    if user_type not in ("C"):
        return {"message": "Você não tem permissão para realizar essa operação."}, 401

    gestor = database.session.query(GESTOR).filter(GESTOR.EMAIL==email).first()

    if gestor: 
        return {"message": "Já existe um cadastro para esse e-mail"}, 406

    gestor = GESTOR(USUARIO=name, EMAIL=email, SENHA=bcrypt.generate_password_hash(password))

    database.session.add(gestor)

    database.session.commit()

    return {"message": "Cadastro realizado com sucesso."}, 200

def edit_manager(manager_id, name, email, password, user_email, user_type):
    if (user_type in ("C")) or (user_email == email):
        valid_email = database.session.query(GESTOR).filter(GESTOR.id!=manager_id, GESTOR.EMAIL==email).first()
        if valid_email:
            return {"message":"Esse email já está em uso, caso necessario pode ser feita a alteração do mesmo."}, 406

        gestor = database.session.query(GESTOR).filter(GESTOR.id==manager_id).first()

        gestor.USUARIO=name
        gestor.EMAIL=email
        gestor.SENHA=bcrypt.generate_password_hash(password)

        database.session.commit()

        return {"message": "Cadastro alterado com sucesso."}, 200
        
        
    return {"message": "Você não tem permissão para realizar essa operação."}, 401


def delete_manager(manager_id, user_type):
    if user_type not in ("C"):
        return {"message": "Você não tem permissão para realizar essa operação."}, 401

    gestor = database.session.query(GESTOR).filter(GESTOR.id==manager_id).first()
    time = database.session.query(TIME).filter(TIME.GESTOR_ID==gestor.id).first()

    if time: 
        return {"message": f"Esse gestor está vinculado ao time {time.NOME}, desvincule-o para excluir esse gestor."}, 406

    database.session.delete(gestor)

    database.session.commit()

    return {"message": "Cadastro excluido com sucesso."}, 200

def list_manager(user_type):
    if user_type not in ("H", "G", "C"):
        return {"message": "Você não tem permissão para realizar essa operação."}, 401


    gestores = GESTOR.query.order_by(GESTOR.USUARIO).all()

    result = []

    for gestor in gestores:
        result.append({
            "id": gestor.id,
            "name": gestor.USUARIO,
            "email": gestor.EMAIL,
        })

    return result