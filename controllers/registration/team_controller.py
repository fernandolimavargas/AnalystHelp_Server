from models.models import ANALISTA, HELPER, GESTOR, TIME

from extensions.database import database

def registration_team(name, helper_id, manager_id, user_type):
    if user_type not in ("G", "C"):
        return {"message": "Você não tem permissão para realizar essa operação."}, 401

    team = TIME(NOME=name, GESTOR_ID=manager_id, HELPER_ID=helper_id)

    database.session.add(team)

    database.session.commit()

    return {"message": "Cadastro realizado com sucesso."}, 200

def edit_team(team_id, name, helper_id, manager_id, user_type):
    if user_type not in ("G", "C"):
        return {"message": "Você não tem permissão para realizar essa operação."}, 401
    
    team = database.session.query(TIME).filter(TIME.id==team_id).first()

    team.NOME=name
    team.GESTOR_ID=manager_id
    team.HELPER_ID=helper_id

    database.session.commit()

    return {"message": "Cadastro alterado com sucesso."}, 200

def delete_team(team_id, user_type):
    if user_type not in ("G", "C"):
        return {"message": "Você não tem permissão para realizar essa operação."}, 401
    
    team = database.session.query(TIME).filter(TIME.id==team_id).first()

    analista = database.session.query(ANALISTA).filter(ANALISTA.TIME_ID==team.id).first()

    if analista:
        return {"message": f"O analista {analista.USUARIO} está vinculado a esse time, desvincule-o para excluir esse time."}, 406

    database.session.delete(team)

    database.session.commit()

    return {"message": "Cadastro excluido com sucesso."}, 200



def list_teams(user_type):
    if user_type not in ("H", "G", "C"):
        return {"message": "Você não tem permissão para realizar essa operação."}, 401

    teams = database.session.query(TIME).order_by(TIME.NOME).all()

    result = []

    for team in teams:
        gestor = database.session.query(GESTOR).filter(GESTOR.id==team.GESTOR_ID).first()
        helper = database.session.query(HELPER).filter(HELPER.id==team.HELPER_ID).first()

        result.append({
            "id_team": team.id,
            "name": team.NOME,
            "gestor": gestor.USUARIO,
            "helper": helper.USUARIO,
            "gestor_id": gestor.id,
            "helper_id": helper.id
        })

    return result