from flask import jsonify
from models.models import (
    SOL_ERRO,
    SOL_ALTERACAO,
    SOL_CUSTOMIZACAO,
    SOL_SERVICO,
    SOL_SCRIPT,
    SOL_IMPORT,
    SOL_SHARE,
    SOL_ISSUE_INT,
    SOL_TICKET,
    HELP,
    USUARIO,
    NOTIFICACAO,
    TIME,
    CONTROLE_TPS_GERAIS,
    CONTROLE_TPS_ANALISTAS,
    BASES,
    REQUEST_BUG
)

from extensions.database import database
from extensions.database_help import database_help
from datetime import date, datetime, timedelta
from calendar import monthrange
from workadays import workdays as wd


def busca_inf_cards_sol(user_id, user_type):

    if user_type == 'C':
        erro_aberto = SOL_ERRO.query.filter(
            SOL_ERRO.STATUS.notin_(['FINALIZADA', 'NÃO APROVADO'])).count()
        erro_fechado = SOL_ERRO.query.filter(
            SOL_ERRO.STATUS.in_(['FINALIZADA', 'NÃO APROVADO'])).count()
        alteracao_aberto = SOL_ALTERACAO.query.filter(
            SOL_ALTERACAO.STATUS.notin_(['FINALIZADA', 'NÃO APROVADO'])).count()
        alteracao_fechado = SOL_ALTERACAO.query.filter(
            SOL_ALTERACAO.STATUS.in_(['FINALIZADA', 'NÃO APROVADO'])).count()
        customizacao_aberto = SOL_CUSTOMIZACAO.query.filter(
            SOL_CUSTOMIZACAO.STATUS.notin_(['FINALIZADA', 'NÃO APROVADO'])).count()
        customizacao_fechado = SOL_CUSTOMIZACAO.query.filter(
            SOL_CUSTOMIZACAO.STATUS.in_(['FINALIZADA', 'NÃO APROVADO'])).count()
        script_aberto = SOL_SCRIPT.query.filter(
            SOL_SCRIPT.STATUS.notin_(['FINALIZADA', 'NÃO APROVADO'])).count()
        script_fechado = SOL_SCRIPT.query.filter(
            SOL_SCRIPT.STATUS.in_(['FINALIZADA', 'NÃO APROVADO'])).count()
        servico_aberto = SOL_SERVICO.query.filter(
            SOL_SERVICO.STATUS.notin_(['FINALIZADA', 'NÃO APROVADO'])).count()
        servico_fechado = SOL_SERVICO.query.filter(
            SOL_SERVICO.STATUS.in_(['FINALIZADA', 'NÃO APROVADO'])).count()
        import_aberto = SOL_IMPORT.query.filter(
            SOL_IMPORT.STATUS.notin_(['FINALIZADA', 'NÃO APROVADO'])).count()
        import_fechado = SOL_IMPORT.query.filter(
            SOL_IMPORT.STATUS.in_(['FINALIZADA', 'NÃO APROVADO'])).count()
        share_aberto = SOL_SHARE.query.filter(
            SOL_SHARE.STATUS.notin_(['FINALIZADA', 'NÃO APROVADO'])).count()
        share_fechado = SOL_SHARE.query.filter(
            SOL_SHARE.STATUS.in_(['FINALIZADA', 'NÃO APROVADO'])).count()
        ticket_aberto = SOL_TICKET.query.filter(
            SOL_TICKET.STATUS.notin_(['FINALIZADA', 'NÃO APROVADO'])).count()
        ticket_fechado = SOL_TICKET.query.filter(
            SOL_TICKET.STATUS.in_(['FINALIZADA', 'NÃO APROVADO'])).count()
        issue_interna_aberto = SOL_ISSUE_INT.query.filter(
            SOL_ISSUE_INT.STATUS.notin_(['FINALIZADA', 'NÃO APROVADO'])).count()
        issue_interna_fechado = SOL_ISSUE_INT.query.filter(
            SOL_ISSUE_INT.STATUS.in_(['FINALIZADA', 'NÃO APROVADO'])).count()
        help_aberto = HELP.query.filter(
            HELP.STATUS.notin_(['FINALIZADA', 'CANCELADO'])).count()
        help_fechado = HELP.query.filter(
            HELP.STATUS.in_(['FINALIZADA', 'CANCELADO'])).count()

    elif user_type == 'G':
        erro_aberto = SOL_ERRO.query.filter(
            SOL_ERRO.STATUS.notin_(['FINALIZADA', 'NÃO APROVADO'])).join(
            USUARIO.query.filter().join(
                TIME.query.filter_by(GESTOR_ID=user_id))).count()
        erro_fechado = SOL_ERRO.query.filter(
            SOL_ERRO.STATUS.in_(['FINALIZADA', 'NÃO APROVADO'])).join(
            USUARIO.query.filter().join(
                TIME.query.filter_by(GESTOR_ID=user_id))).count()
        alteracao_aberto = SOL_ALTERACAO.query.filter(
            SOL_ALTERACAO.STATUS.notin_(['FINALIZADA', 'NÃO APROVADO'])).join(
            USUARIO.query.filter().join(
                TIME.query.filter_by(GESTOR_ID=user_id))).count()
        alteracao_fechado = SOL_ALTERACAO.query.filter(
            SOL_ALTERACAO.STATUS.in_(['FINALIZADA', 'NÃO APROVADO'])).join(
            USUARIO.query.filter().join(
                TIME.query.filter_by(GESTOR_ID=user_id))).count()
        customizacao_aberto = SOL_CUSTOMIZACAO.query.filter(
            SOL_CUSTOMIZACAO.STATUS.notin_(['FINALIZADA', 'NÃO APROVADO'])).join(
            USUARIO.query.filter().join(
                TIME.query.filter_by(GESTOR_ID=user_id))).count()
        customizacao_fechado = SOL_CUSTOMIZACAO.query.filter(
            SOL_CUSTOMIZACAO.STATUS.in_(['FINALIZADA', 'NÃO APROVADO'])).join(
            USUARIO.query.filter().join(
                TIME.query.filter_by(GESTOR_ID=user_id))).count()
        script_aberto = SOL_SCRIPT.query.filter(
            SOL_SCRIPT.STATUS.notin_(['FINALIZADA', 'NÃO APROVADO'])).join(
            USUARIO.query.filter().join(
                TIME.query.filter_by(GESTOR_ID=user_id))).count()
        script_fechado = SOL_SCRIPT.query.filter(
            SOL_SCRIPT.STATUS.in_(['FINALIZADA', 'NÃO APROVADO'])).join(
            USUARIO.query.filter().join(
                TIME.query.filter_by(GESTOR_ID=user_id))).count()
        servico_aberto = SOL_SERVICO.query.filter(
            SOL_SERVICO.STATUS.notin_(['FINALIZADA', 'NÃO APROVADO'])).join(
            USUARIO.query.filter().join(
                TIME.query.filter_by(GESTOR_ID=user_id))).count()
        servico_fechado = SOL_SERVICO.query.filter(
            SOL_SERVICO.STATUS.in_(['FINALIZADA', 'NÃO APROVADO'])).join(
            USUARIO.query.filter().join(
                TIME.query.filter_by(GESTOR_ID=user_id))).count()
        import_aberto = SOL_IMPORT.query.filter(
            SOL_IMPORT.STATUS.notin_(['FINALIZADA', 'NÃO APROVADO'])).join(
            USUARIO.query.filter().join(
                TIME.query.filter_by(GESTOR_ID=user_id))).count()
        import_fechado = SOL_IMPORT.query.filter(
            SOL_IMPORT.STATUS.in_(['FINALIZADA', 'NÃO APROVADO'])).join(
            USUARIO.query.filter().join(
                TIME.query.filter_by(GESTOR_ID=user_id))).count()
        share_aberto = SOL_SHARE.query.filter(
            SOL_SHARE.STATUS.notin_(['FINALIZADA', 'NÃO APROVADO'])).join(
            USUARIO.query.filter().join(
                TIME.query.filter_by(GESTOR_ID=user_id))).count()
        share_fechado = SOL_SHARE.query.filter(
            SOL_SHARE.STATUS.in_(['FINALIZADA', 'NÃO APROVADO'])).join(
            USUARIO.query.filter().join(
                TIME.query.filter_by(GESTOR_ID=user_id))).count()
        ticket_aberto = SOL_TICKET.query.filter(
            SOL_TICKET.STATUS.notin_(['FINALIZADA', 'NÃO APROVADO'])).join(
            USUARIO.query.filter().join(
                TIME.query.filter_by(GESTOR_ID=user_id))).count()
        ticket_fechado = SOL_TICKET.query.filter(
            SOL_TICKET.STATUS.in_(['FINALIZADA', 'NÃO APROVADO'])).join(
            USUARIO.query.filter().join(
                TIME.query.filter_by(GESTOR_ID=user_id))).count()
        issue_interna_aberto = SOL_ISSUE_INT.query.filter(
            SOL_ISSUE_INT.STATUS.notin_(['FINALIZADA', 'NÃO APROVADO'])).join(
            USUARIO.query.filter().join(
                TIME.query.filter_by(GESTOR_ID=user_id))).count()
        issue_interna_fechado = SOL_ISSUE_INT.query.filter(
            SOL_ISSUE_INT.STATUS.in_(['FINALIZADA', 'NÃO APROVADO'])).join(
            USUARIO.query.filter().join(
                TIME.query.filter_by(GESTOR_ID=user_id))).count()
        help_aberto = HELP.query.filter(
            HELP.STATUS.notin_(['FINALIZADA', 'CANCELADO'])).join(
            USUARIO.query.filter().join(
                TIME.query.filter_by(GESTOR_ID=user_id))).count()
        help_fechado = HELP.query.filter(
            HELP.STATUS.in_(['FINALIZADA', 'CANCELADO'])).join(
            USUARIO.query.filter().join(
                TIME.query.filter_by(GESTOR_ID=user_id))).count()
    elif user_type == 'H':
        erro_aberto = SOL_ERRO.query.filter(
            SOL_ERRO.STATUS.notin_(['FINALIZADA', 'NÃO APROVADO']),
            SOL_ERRO.HELPER_ID == user_id).count()
        erro_fechado = SOL_ERRO.query.filter(
            SOL_ERRO.STATUS.in_(['FINALIZADA', 'NÃO APROVADO']),
            SOL_ERRO.HELPER_ID == user_id).count()
        alteracao_aberto = SOL_ALTERACAO.query.filter(
            SOL_ALTERACAO.STATUS.notin_(['FINALIZADA', 'NÃO APROVADO']),
            SOL_ALTERACAO.HELPER_ID == user_id).count()
        alteracao_fechado = SOL_ALTERACAO.query.filter(
            SOL_ALTERACAO.STATUS.in_(['FINALIZADA', 'NÃO APROVADO']),
            SOL_ALTERACAO.HELPER_ID == user_id).count()
        customizacao_aberto = SOL_CUSTOMIZACAO.query.filter(
            SOL_CUSTOMIZACAO.STATUS.notin_(['FINALIZADA', 'NÃO APROVADO']),
            SOL_CUSTOMIZACAO.HELPER_ID == user_id).count()
        customizacao_fechado = SOL_CUSTOMIZACAO.query.filter(
            SOL_CUSTOMIZACAO.STATUS.in_(['FINALIZADA', 'NÃO APROVADO']),
            SOL_CUSTOMIZACAO.HELPER_ID == user_id).count()
        script_aberto = SOL_SCRIPT.query.filter(
            SOL_SCRIPT.STATUS.notin_(['FINALIZADA', 'NÃO APROVADO']),
            SOL_SCRIPT.HELPER_ID == user_id).count()
        script_fechado = SOL_SCRIPT.query.filter(
            SOL_SCRIPT.STATUS.in_(['FINALIZADA', 'NÃO APROVADO']),
            SOL_SCRIPT.HELPER_ID == user_id).count()
        servico_aberto = SOL_SERVICO.query.filter(
            SOL_SERVICO.STATUS.notin_(['FINALIZADA', 'NÃO APROVADO']),
            SOL_SERVICO.HELPER_ID == user_id).count()
        servico_fechado = SOL_SERVICO.query.filter(
            SOL_SERVICO.STATUS.in_(['FINALIZADA', 'NÃO APROVADO']),
            SOL_SERVICO.HELPER_ID == user_id).count()
        import_aberto = SOL_IMPORT.query.filter(
            SOL_IMPORT.STATUS.notin_(['FINALIZADA', 'NÃO APROVADO']),
            SOL_IMPORT.HELPER_ID == user_id).count()
        import_fechado = SOL_IMPORT.query.filter(
            SOL_IMPORT.STATUS.in_(['FINALIZADA', 'NÃO APROVADO']),
            SOL_IMPORT.HELPER_ID == user_id).count()
        share_aberto = SOL_SHARE.query.filter(
            SOL_SHARE.STATUS.notin_(['FINALIZADA', 'NÃO APROVADO']),
            SOL_SHARE.HELPER_ID == user_id).count()
        share_fechado = SOL_SHARE.query.filter(
            SOL_SHARE.STATUS.in_(['FINALIZADA', 'NÃO APROVADO']),
            SOL_SHARE.HELPER_ID == user_id).count()
        ticket_aberto = SOL_TICKET.query.filter(
            SOL_TICKET.STATUS.notin_(['FINALIZADA', 'NÃO APROVADO']),
            SOL_TICKET.HELPER_ID == user_id).count()
        ticket_fechado = SOL_TICKET.query.filter(
            SOL_TICKET.STATUS.in_(['FINALIZADA', 'NÃO APROVADO']),
            SOL_TICKET.HELPER_ID == user_id).count()
        issue_interna_aberto = SOL_ISSUE_INT.query.filter(
            SOL_ISSUE_INT.STATUS.notin_(['FINALIZADA', 'NÃO APROVADO']),
            SOL_ISSUE_INT.HELPER_ID == user_id).count()
        issue_interna_fechado = SOL_ISSUE_INT.query.filter(
            SOL_ISSUE_INT.STATUS.in_(['FINALIZADA', 'NÃO APROVADO']),
            SOL_ISSUE_INT.HELPER_ID == user_id).count()
        help_aberto = HELP.query.filter(
            HELP.STATUS.notin_(['FINALIZADA', 'CANCELADO']),
            HELP.HELPER_ID == user_id).count()
        help_fechado = HELP.query.filter(
            HELP.STATUS.in_(['FINALIZADA', 'CANCELADO']),
            HELP.HELPER_ID == user_id).count()
    elif user_type == 'A':
        erro_aberto = SOL_ERRO.query.filter(
            SOL_ERRO.STATUS.notin_(['FINALIZADA', 'NÃO APROVADO']),
            SOL_ERRO.ANALISTA_ID == user_id).count()
        erro_fechado = SOL_ERRO.query.filter(
            SOL_ERRO.STATUS.in_(['FINALIZADA', 'NÃO APROVADO']),
            SOL_ERRO.ANALISTA_ID == user_id).count()
        alteracao_aberto = SOL_ALTERACAO.query.filter(
            SOL_ALTERACAO.STATUS.notin_(['FINALIZADA', 'NÃO APROVADO']),
            SOL_ALTERACAO.ANALISTA_ID == user_id).count()
        alteracao_fechado = SOL_ALTERACAO.query.filter(
            SOL_ALTERACAO.STATUS.in_(['FINALIZADA', 'NÃO APROVADO']),
            SOL_ALTERACAO.ANALISTA_ID == user_id).count()
        customizacao_aberto = SOL_CUSTOMIZACAO.query.filter(
            SOL_CUSTOMIZACAO.STATUS.notin_(['FINALIZADA', 'NÃO APROVADO']),
            SOL_CUSTOMIZACAO.ANALISTA_ID == user_id).count()
        customizacao_fechado = SOL_CUSTOMIZACAO.query.filter(
            SOL_CUSTOMIZACAO.STATUS.in_(['FINALIZADA', 'NÃO APROVADO']),
            SOL_CUSTOMIZACAO.ANALISTA_ID == user_id).count()
        script_aberto = SOL_SCRIPT.query.filter(
            SOL_SCRIPT.STATUS.notin_(['FINALIZADA', 'NÃO APROVADO']),
            SOL_SCRIPT.ANALISTA_ID == user_id).count()
        script_fechado = SOL_SCRIPT.query.filter(
            SOL_SCRIPT.STATUS.in_(['FINALIZADA', 'NÃO APROVADO']),
            SOL_SCRIPT.ANALISTA_ID == user_id).count()
        servico_aberto = SOL_SERVICO.query.filter(
            SOL_SERVICO.STATUS.notin_(['FINALIZADA', 'NÃO APROVADO']),
            SOL_SERVICO.ANALISTA_ID == user_id).count()
        servico_fechado = SOL_SERVICO.query.filter(
            SOL_SERVICO.STATUS.in_(['FINALIZADA', 'NÃO APROVADO']),
            SOL_SERVICO.ANALISTA_ID == user_id).count()
        import_aberto = SOL_IMPORT.query.filter(
            SOL_IMPORT.STATUS.notin_(['FINALIZADA', 'NÃO APROVADO']),
            SOL_IMPORT.ANALISTA_ID == user_id).count()
        import_fechado = SOL_IMPORT.query.filter(
            SOL_IMPORT.STATUS.in_(['FINALIZADA', 'NÃO APROVADO']),
            SOL_IMPORT.ANALISTA_ID == user_id).count()
        share_aberto = SOL_SHARE.query.filter(
            SOL_SHARE.STATUS.notin_(['FINALIZADA', 'NÃO APROVADO']),
            SOL_SHARE.ANALISTA_ID == user_id).count()
        share_fechado = SOL_SHARE.query.filter(
            SOL_SHARE.STATUS.in_(['FINALIZADA', 'NÃO APROVADO']),
            SOL_SHARE.ANALISTA_ID == user_id).count()
        ticket_aberto = SOL_TICKET.query.filter(
            SOL_TICKET.STATUS.notin_(['FINALIZADA', 'NÃO APROVADO']),
            SOL_TICKET.ANALISTA_ID == user_id).count()
        ticket_fechado = SOL_TICKET.query.filter(
            SOL_TICKET.STATUS.in_(['FINALIZADA', 'NÃO APROVADO']),
            SOL_TICKET.ANALISTA_ID == user_id).count()
        issue_interna_aberto = SOL_ISSUE_INT.query.filter(
            SOL_ISSUE_INT.STATUS.notin_(['FINALIZADA', 'NÃO APROVADO']),
            SOL_ISSUE_INT.ANALISTA_ID == user_id).count()
        issue_interna_fechado = SOL_ISSUE_INT.query.filter(
            SOL_ISSUE_INT.STATUS.in_(['FINALIZADA', 'NÃO APROVADO']),
            SOL_ISSUE_INT.ANALISTA_ID == user_id).count()
        help_aberto = HELP.query.filter(
            HELP.STATUS.notin_(['FINALIZADA', 'CANCELADO']),
            HELP.ANALISTA_ID == user_id).count()
        help_fechado = HELP.query.filter(
            HELP.STATUS.in_(['FINALIZADA', 'CANCELADO']),
            HELP.ANALISTA_ID == user_id).count()

    result = [{
        "aberto": erro_aberto,
        "fechado": erro_fechado,
    },
        {
        "aberto": alteracao_aberto,
        "fechado": alteracao_fechado,
    },
        {
        "aberto": customizacao_aberto,
        "fechado": customizacao_fechado,
    },
        {
        "aberto": script_aberto,
        "fechado": script_fechado,
    },
        {
        "aberto": servico_aberto,
        "fechado": servico_fechado,
    },
        {
        "aberto": import_aberto,
        "fechado": import_fechado,
    },
        {
        "aberto": share_aberto,
        "fechado": share_fechado,
    },
        {
        "aberto": ticket_aberto,
        "fechado": ticket_fechado,
    },
        {
        "aberto": issue_interna_aberto,
        "fechado": issue_interna_fechado,
    },
        {
        "aberto": help_aberto,
        "fechado": help_fechado,
    }]

    return result


def busca_inf_filas(user_id, user_type, user_email):
    if user_type == 'A':
        tps = database_help.execute(f"""
        SELECT [dbo].[controle_tps_analistas].[nro_tp],
            [dbo].[controle_tps_analistas].[issue],
            [dbo].[usuario].[nome],
            [dbo].[time].[nome],
            [dbo].[controle_tps_analistas].[grupo],
            [dbo].[controle_tps_analistas].[resumo],
            [dbo].[controle_tps_analistas].[dias_aberto],
            Datediff(day, [dbo].[controle_tps_analistas].[dta_ult_mov], Getdate()) AS
            ULT_MOV,
            [dbo].[controle_tps_analistas].[status],
            [dbo].[controle_tps_analistas].[prioridade],
            CASE
                WHEN [dbo].[controle_tps_analistas].[dta_fim] < Getdate() THEN 'S'
                WHEN [dbo].[controle_tps_analistas].[dta_fim] > Getdate() THEN 'N'
                ELSE 'N'
            END AS
            BACKLOG
        FROM   [dbo].[controle_tps_analistas]
            INNER JOIN [dbo].[usuario]
                    ON ( [dbo].[usuario].[email] =
                        [dbo].[controle_tps_analistas].[analista] )
            INNER JOIN [dbo].[time]
                    ON ( [dbo].[time].[id] = [dbo].[usuario].[time_id] )
        WHERE  [dbo].[usuario].[email] = '{user_email}';""").fetchall()

        result = []

        for tp in tps:
            result.append({
                "nroTp": tp[0],
                "issue": tp[1],
                "analista": tp[2],
                "time": tp[3],
                "grupo": tp[4].split('-')[0].title(),
                "resumo": tp[5].strip(),
                "diasAberto": tp[6],
                "dtaUltMov": tp[7],
                "status": tp[8].strip().title(),
                "prioridade": tp[9],
                "backlog": tp[10]
            })

    else:
        if user_type == 'C':
            times = TIME.query.all()
        elif user_type == 'G':
            times = TIME.query.filter_by(GESTOR_ID=user_id).all()
        elif user_type == 'H':
            times = TIME.query.filter_by(HELPER_ID=user_id).all()

        lista_times = []

        for i in times:
            lista_times.append(i.id)

        tps = database.session.query(CONTROLE_TPS_ANALISTAS, USUARIO, TIME).filter(
            USUARIO.TIME_ID.in_(lista_times),
            USUARIO.EMAIL == CONTROLE_TPS_ANALISTAS.ANALISTA,
            TIME.id == USUARIO.TIME_ID).all()

        lista_times = r", ".join(map(str, lista_times))
        
        tps = database_help.execute(f"""
        SELECT [dbo].[controle_tps_analistas].[nro_tp],
            [dbo].[controle_tps_analistas].[issue],
            [dbo].[usuario].[nome],
            [dbo].[time].[nome],
            [dbo].[controle_tps_analistas].[grupo],
            [dbo].[controle_tps_analistas].[resumo],
            [dbo].[controle_tps_analistas].[dias_aberto],
            Datediff(day, [dbo].[controle_tps_analistas].[dta_ult_mov], Getdate()) AS
            ULT_MOV,
            [dbo].[controle_tps_analistas].[status],
            [dbo].[controle_tps_analistas].[prioridade],
            CASE
                WHEN [dbo].[controle_tps_analistas].[dta_fim] < Getdate() THEN 'S'
                WHEN [dbo].[controle_tps_analistas].[dta_fim] > Getdate() THEN 'N'
                ELSE 'N'
            END AS
            BACKLOG
        FROM   [dbo].[controle_tps_analistas]
            INNER JOIN [dbo].[usuario]
                    ON ( [dbo].[usuario].[email] =
                        [dbo].[controle_tps_analistas].[analista] )
            INNER JOIN [dbo].[time]
                    ON ( [dbo].[time].[id] = [dbo].[usuario].[time_id] )
        WHERE  [dbo].[time].[id] IN ({lista_times});""").fetchall()

        result = []

        for tp in tps:
            result.append({
                "nroTp": tp[0],
                "issue": tp[1],
                "analista": tp[2],
                "time": tp[3],
                "grupo": tp[4].split('-')[0].title(),
                "resumo": tp[5].strip(),
                "diasAberto": tp[6],
                "dtaUltMov": tp[7],
                "status": tp[8].strip().title(),
                "prioridade": tp[9],
                "backlog": tp[10]
            })

        return result

    return result


def busca_inf_filas_gerais():
    info_tps = CONTROLE_TPS_GERAIS.query.first()

    result = jsonify(
        {"id": "1",
            "name": "Apollo",
            "P0": info_tps.APOLLO_p0,
            "P1": info_tps.APOLLO_p1,
            "P2": info_tps.APOLLO_p2,
            "P3": info_tps.APOLLO_p3,
            "qtd_tp": info_tps.APOLLO_tot
         },
        {"id": "2",
            "name": "Bravos",
            "P0": info_tps.BRAVOS_p0,
            "P1": info_tps.BRAVOS_p1,
            "P2": info_tps.BRAVOS_p2,
            "P3": info_tps.BRAVOS_p3,
            "qtd_tp": info_tps.BRAVOS_tot
         },
        {"id": "3",
            "name": "Toyota",
            "P0": info_tps.TOYOTA_p0,
            "P1": info_tps.TOYOTA_p1,
            "P2": info_tps.TOYOTA_p2,
            "P3": info_tps.TOYOTA_p3,
            "qtd_tp": info_tps.TOYOTA_tot
         },
        {"id": "4",
            "name": "Autoshop",
            "P0": info_tps.AUTOSHOP_p0,
            "P1": info_tps.AUTOSHOP_p1,
            "P2": info_tps.AUTOSHOP_p2,
            "P3": info_tps.AUTOSHOP_p3,
            "qtd_tp": info_tps.AUTOSHOP_tot
         },
        {"id": "5",
            "name": "Berçário",
            "P0": info_tps.BERCARIO_p0,
            "P1": info_tps.BERCARIO_p1,
            "P2": info_tps.BERCARIO_p2,
            "P3": info_tps.BERCARIO_p3,
            "qtd_tp": info_tps.BERCARIO_tot
         },
        {"id": "6",
            "name": "Financeiro",
            "P0": info_tps.FINANCEIRO_p0,
            "P1": info_tps.FINANCEIRO_p1,
            "P2": info_tps.FINANCEIRO_p2,
            "P3": info_tps.FINANCEIRO_p3,
            "qtd_tp": info_tps.FINANCEIRO_tot
         },
        {"id": "7",
            "name": "NFSE/NFCE",
            "P0": info_tps.NFCE_p0,
            "P1": info_tps.NFCE_p1,
            "P2": info_tps.NFCE_p2,
            "P3": info_tps.NFCE_p3,
            "qtd_tp": info_tps.NFCE_tot
         },
        {"id": "8",
            "name": "Montadoras",
            "P0": info_tps.MONTADORA_p0,
            "P1": info_tps.MONTADORA_p1,
            "P2": info_tps.MONTADORA_p2,
            "P3": info_tps.MONTADORA_p3,
            "qtd_tp": info_tps.MONTADORA_tot
         },
        {"id": "9",
            "name": "Mobile",
            "P0": info_tps.MOBILE_p0,
            "P1": info_tps.MOBILE_p1,
            "P2": info_tps.MOBILE_p2,
            "P3": info_tps.MOBILE_p3,
            "qtd_tp": info_tps.MOBILE_tot
         },
        {"id": "10",
            "name": "Contábil/Fiscal",
            "P0": info_tps.CONTABIL_p0,
            "P1": info_tps.CONTABIL_p1,
            "P2": info_tps.CONTABIL_p2,
            "P3": info_tps.CONTABIL_p3,
            "qtd_tp": info_tps.CONTABIL_tot
         },
        {"id": "11",
            "name": "CC1",
            "P0": info_tps.CC1_p0,
            "P1": info_tps.CC1_p1,
            "P2": info_tps.CC1_p2,
            "P3": info_tps.CC1_p3,
            "qtd_tp": info_tps.CC1_tot
         }
    )

    return result

def busca_inf_filas_analitic(user_id, user_type):
    data_atual = date.today()
    dt2 = data_atual.replace(day=1) + timedelta(monthrange(data_atual.year, data_atual.month)[1])
    dt1 = data_atual.replace(day=1)
    dias_uteis = wd.networkdays(dt1, dt2)
    
    if user_type == 'A':
        result = {'message': 'em desenvolvimento'}

    else:
        if user_type == 'C':
            times = TIME.query.all()
        if user_type == 'G':
            times = TIME.query.filter_by(GESTOR_ID=user_id).all()
        elif user_type == 'H':
            times = TIME.query.filter_by(HELPER_ID=user_id).all()

        lista_times = []

        for i in times:
            lista_times.append(i.id)

        lista_times = r", ".join(map(str, lista_times))

    result_database = database_help.execute(f"""select  distinct [dbo].[usuario].[nome],
                            [dbo].[time].[nome],
                            (select Count ( [dbo].[controle_tps_analistas].[nro_tp]) from [dbo].[controle_tps_analistas]
                            where [dbo].[usuario].[email] = [dbo].[controle_tps_analistas].[analista]) as geral,
                        (select Count ( [dbo].[controle_tps_analistas].[nro_tp]) from [dbo].[controle_tps_analistas]
                            where [dbo].[usuario].[email] = [dbo].[controle_tps_analistas].[analista]
                        and [dbo].[controle_tps_analistas].[issue] like '%AUTO%') as issue,
                        (select Count ( [dbo].[controle_tps_analistas].[nro_tp]) from [dbo].[controle_tps_analistas]
                            where [dbo].[usuario].[email] = [dbo].[controle_tps_analistas].[analista]
                        and [dbo].[controle_tps_analistas].[dias_aberto] >= 15) as mais_15,
                        (select Count ( [dbo].[controle_tps_analistas].[nro_tp]) from [dbo].[controle_tps_analistas]
                            where [dbo].[usuario].[email] = [dbo].[controle_tps_analistas].[analista]
                        and [dbo].[controle_tps_analistas].[issue] not like '%AUTO%'
                        and [dbo].[controle_tps_analistas].dta_fim < getdate()) as backlog,
                            Format(( 100 * Cast(
                                        [dbo].[controle_tps_analistas_analitico].[atingimento] AS
                                        NUMERIC(3
                                        ))
                                            / ( {dias_uteis} * [dbo].[usuario].[meta] ) ), '0.00') AS
                            ATINGIMENTO,
                            [dbo].[controle_tps_analistas_analitico].[perc_reabertos],
                            [dbo].[controle_tps_analistas_analitico].[sla],
                            [dbo].[controle_tps_analistas_analitico].[perc_respostas],
                            [dbo].[controle_tps_analistas_analitico].[nps]
            from [dbo].[controle_tps_analistas]
            left join [dbo].[controle_tps_analistas_analitico] on
            ( [dbo].[controle_tps_analistas_analitico].[analista] + '@linx.com.br' = upper([dbo].[controle_tps_analistas].[analista]))
            inner join [dbo].[usuario] on 
            ( [dbo].[usuario].[email] = [dbo].[controle_tps_analistas].[analista] )
            inner join [dbo].[time] on 
            ( [dbo].[time].[id] = [dbo].[usuario].[time_id])
            WHERE  [dbo].[usuario].[tipo] = 'A'
                AND [dbo].[usuario].[inativo] = 'N'
				AND [dbo].[time].[id] in ({lista_times})""").fetchall()

    result = []
    for value in result_database:
        

        result.append({
            "analista": value[0],
            "time": value[1],
            "qtdFila": value[2],
            "qtdIssue": value[3],
            "qtdMais": value[4],
            "qtdBacklog": value[5],
            "ating": value[6],
            "abert": value[7],
            "sla": value[8],
            "res": value[9],
            "nps": value[10],
        })
    
    return result


def busca_inf_filas_footer(user_id, user_type):
    if user_type == 'A':
        result_database = database_help.execute(f"""
        SELECT DISTINCT (SELECT Count([dbo].[controle_tps_analistas].[nro_tp])
                        FROM   [dbo].[controle_tps_analistas]
                        WHERE  [dbo].[controle_tps_analistas].[analista] =
                                [dbo].[usuario].[email]) AS
                        geral,
                        (SELECT Count(nro_tp)
                        FROM   [dbo].[controle_tps_analistas]
                        WHERE  [dbo].[controle_tps_analistas].[analista] =
                                [dbo].[usuario].[email]
                                AND [dbo].[controle_tps_analistas].[issue] LIKE '%AUTO%'
                        )            AS issue,
                        (SELECT Count(nro_tp)
                        FROM   [dbo].[controle_tps_analistas]
                        WHERE  [dbo].[controle_tps_analistas].[analista] =
                                [dbo].[usuario].[email]
                                AND [dbo].[controle_tps_analistas].[dias_aberto] >= 15)
                        AS mais_15,
                        (SELECT Count(nro_tp)
                        FROM   [dbo].[controle_tps_analistas]
                        WHERE  [dbo].[controle_tps_analistas].[analista] =
                                [dbo].[usuario].[email]
                                AND [dbo].[controle_tps_analistas].[issue] NOT LIKE
                                    '%AUTO%'
                                AND [dbo].[controle_tps_analistas].[dta_fim] < Getdate()
                        )            AS backlog
        FROM   [dbo].[controle_tps_analistas]
            INNER JOIN [dbo].[usuario]
                    ON ( [dbo].[controle_tps_analistas].[analista] =
                        [dbo].[usuario].[email] )
        WHERE [dbo].[usuario].[id] in ({user_id})""").fetchall()

        result = []
        
        result.append({
            "qtdFila": result_database[0][0],
            "qtdIssue": result_database[0][1],
            "qtdMais": result_database[0][2],
            "qtdBacklog": result_database[0][3]
        })

    else:
        if user_type == 'C':
            times = TIME.query.all()
        if user_type == 'G':
            times = TIME.query.filter_by(GESTOR_ID=user_id).all()
        elif user_type == 'H':
            times = TIME.query.filter_by(HELPER_ID=user_id).all()

        lista_times = []

        for i in times:
            lista_times.append(i.id)

        lista_times = r", ".join(map(str, lista_times))

        result_database = database_help.execute(f"""
            SELECT DISTINCT (SELECT Count([dbo].[controle_tps_analistas].[nro_tp])
                            FROM   [dbo].[controle_tps_analistas]
                            WHERE  [dbo].[controle_tps_analistas].[analista] =
                                    [dbo].[usuario].[email]) AS
                            geral,
                            (SELECT Count(nro_tp)
                            FROM   [dbo].[controle_tps_analistas]
                            WHERE  [dbo].[controle_tps_analistas].[analista] =
                                    [dbo].[usuario].[email]
                                    AND [dbo].[controle_tps_analistas].[issue] LIKE '%AUTO%'
                            )            AS issue,
                            (SELECT Count(nro_tp)
                            FROM   [dbo].[controle_tps_analistas]
                            WHERE  [dbo].[controle_tps_analistas].[analista] =
                                    [dbo].[usuario].[email]
                                    AND [dbo].[controle_tps_analistas].[dias_aberto] >= 15)
                            AS mais_15,
                            (SELECT Count(nro_tp)
                            FROM   [dbo].[controle_tps_analistas]
                            WHERE  [dbo].[controle_tps_analistas].[analista] =
                                    [dbo].[usuario].[email]
                                    AND [dbo].[controle_tps_analistas].[issue] NOT LIKE
                                        '%AUTO%'
                                    AND [dbo].[controle_tps_analistas].[dta_fim] < Getdate()
                            )            AS backlog
            FROM   [dbo].[controle_tps_analistas]
                INNER JOIN [dbo].[usuario]
                        ON ( [dbo].[controle_tps_analistas].[analista] =
                            [dbo].[usuario].[email] )
                INNER JOIN [dbo].[time]
                        ON ( [dbo].[time].id = [dbo].[usuario].[time_id] )
            WHERE [dbo].[time].[id] in ({lista_times})""").fetchall()

        geral = 0 
        issue = 0 
        mais_15 = 0 
        backlog = 0

        for i in result_database:
            geral += i[0]
            issue += i[1]
            mais_15 += i[2]
            backlog += i[3]

        result = []

        result.append({
            "qtdFila": geral,
            "qtdIssue": issue,
            "qtdMais": mais_15,
            "qtdBacklog": backlog
        })
    
    return result


def request_bug_create(user_id, what, how, obs, req_type):
    new_request = REQUEST_BUG(SOLICITANTE=user_id, OQUE=what,
                              COMO=how, OBS=obs, TIPO=req_type, STATUS='NÃO INICIADO')

    database.session.add(new_request)
    database.session.commit()

    return {'message': 'Solicitação enviada com sucesso, agradecemos sua colaboração!'}, 200

def notification_list(user_id):
    notifications = database.session.query(NOTIFICACAO).filter(
        NOTIFICACAO.USUARIO_ID == user_id,
        NOTIFICACAO.STATUS == 'N').all()

    result = []

    for notification in notifications:
        result.append({
            "notificationId": notification.id,
            "type": notification.TIPO,
            "subType": notification.SUBTIPO,
            "message": notification.MENSAGEM,
            "status": notification.STATUS,
            "dtaCreate": notification.DTA_CREATE.strftime("%d/%m/%Y %H:%M:%S")
        })


    return result

def notification_reading(notification_id):
    notification = database.session.query(NOTIFICACAO).filter(
        NOTIFICACAO.id == notification_id).first()

    notification.STATUS = 'L'

    database.session.commit()

    return {"message": "Mensagem lida"}