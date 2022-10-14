from models.models import ANALISTA, HELPER, GESTOR, BASES

from extensions.database import database

def registration_database(client, 
        charset, 
        server, 
        structure, 
        instance,
        db_user,
        brands,
        size, 
        dta_dmpbak,
        user_type):

    if user_type not in ("H", "G", "C"):
        return {"message": "Você não tem permissão para realizar essa operação."}, 401

    db_register = BASES(CLIENTE=client, 
        CHARSET=charset, 
        SERVIDOR=server,
        ESTRUTURA=structure,
        INSTANCIA=instance,
        USUARIO=db_user,
        MARCA=brands,
        TAMANHO=size,
        DTA_DMPBAK=dta_dmpbak)

    database.session.add(db_register)

    database.session.commit()

    return {"message": "Cadastro realizado com sucesso."}, 200

def edit_database(db_id, 
        client, 
        charset, 
        server, 
        structure, 
        instance,
        db_user,
        brands,
        size, 
        dta_dmpbak,
        user_type):
    if user_type not in ("H", "G", "C"):
        return {"message": "Você não tem permissão para realizar essa operação."}, 401

    db_register = database.session.query(BASES).filter(BASES.id==db_id).first()

    db_register.CLIENTE=client
    db_register.CHARSET=charset
    db_register.SERVIDOR=server
    db_register.ESTRUTURA=structure
    db_register.INSTANCIA=instance
    db_register.USUARIO=db_user
    db_register.MARCA=brands
    db_register.TAMANHO=size
    db_register.DTA_DMPBAK=dta_dmpbak

    database.session.commit()

    return {"message": "Cadastro alterado com sucesso."}, 200

def delete_database(db_id, user_type):
    if user_type not in ("H", "G", "C"):
        return {"message": "Você não tem permissão para realizar essa operação."}, 401

    db_register = database.session.query(BASES).filter(BASES.id==db_id).first()

    database.session.delete(db_register)

    database.session.commit()

    return {"message": "Cadastro excluido com sucesso."}, 200


def list_database(user_type):
    if user_type not in ("A", "H", "G", "C"):
        return {"message": "Você não tem permissão para realizar essa operação."}, 401
    bases = BASES.query.all()

    result = []

    for base in bases:
        result.append({
            "id": base.id,
            "name": base.CLIENTE,
            "charset": base.CHARSET,
            "server": base.SERVIDOR,
            "structure": base.ESTRUTURA,
            "instance": base.INSTANCIA,
            "dbUser": base.USUARIO,
            "brands": base.MARCA,
            "size": base.TAMANHO,
            "dtaDmpBak": base.DTA_DMPBAK.strftime("%Y-%d-%m")
        })

    return result