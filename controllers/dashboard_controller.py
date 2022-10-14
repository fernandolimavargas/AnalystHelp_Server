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
    ANALISTA,
    HELPER,
    GESTOR,
    TIME,
    CONTROLE_TPS_GERAIS,
    CONTROLE_TPS_ANALISTAS,
    BASES,
    REQUEST_BUG
)

from extensions.database import database
from extensions.databaseazure import database_azure
from datetime import date, timedelta
from calendar import monthrange
from workadays import workdays


def busca_inf_cards_sol(user_id, user_type):

    if user_type== 'C':
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

    elif user_type== 'G':
        erro_aberto = SOL_ERRO.query.filter(
            SOL_ERRO.STATUS.notin_(['FINALIZADA', 'NÃO APROVADO'])).join(
            ANALISTA.query.filter().join(
                TIME.query.filter_by(GESTOR_ID=user_id))).count()
        erro_fechado = SOL_ERRO.query.filter(
            SOL_ERRO.STATUS.in_(['FINALIZADA', 'NÃO APROVADO'])).join(
            ANALISTA.query.filter().join(
                TIME.query.filter_by(GESTOR_ID=user_id))).count()
        alteracao_aberto = SOL_ALTERACAO.query.filter(
            SOL_ALTERACAO.STATUS.notin_(['FINALIZADA', 'NÃO APROVADO'])).join(
            ANALISTA.query.filter().join(
                TIME.query.filter_by(GESTOR_ID=user_id))).count()
        alteracao_fechado = SOL_ALTERACAO.query.filter(
            SOL_ALTERACAO.STATUS.in_(['FINALIZADA', 'NÃO APROVADO'])).join(
            ANALISTA.query.filter().join(
                TIME.query.filter_by(GESTOR_ID=user_id))).count()
        customizacao_aberto = SOL_CUSTOMIZACAO.query.filter(
            SOL_CUSTOMIZACAO.STATUS.notin_(['FINALIZADA', 'NÃO APROVADO'])).join(
            ANALISTA.query.filter().join(
                TIME.query.filter_by(GESTOR_ID=user_id))).count()
        customizacao_fechado = SOL_CUSTOMIZACAO.query.filter(
            SOL_CUSTOMIZACAO.STATUS.in_(['FINALIZADA', 'NÃO APROVADO'])).join(
            ANALISTA.query.filter().join(
                TIME.query.filter_by(GESTOR_ID=user_id))).count()
        script_aberto = SOL_SCRIPT.query.filter(
            SOL_SCRIPT.STATUS.notin_(['FINALIZADA', 'NÃO APROVADO'])).join(
            ANALISTA.query.filter().join(
                TIME.query.filter_by(GESTOR_ID=user_id))).count()
        script_fechado = SOL_SCRIPT.query.filter(
            SOL_SCRIPT.STATUS.in_(['FINALIZADA', 'NÃO APROVADO'])).join(
            ANALISTA.query.filter().join(
                TIME.query.filter_by(GESTOR_ID=user_id))).count()
        servico_aberto = SOL_SERVICO.query.filter(
            SOL_SERVICO.STATUS.notin_(['FINALIZADA', 'NÃO APROVADO'])).join(
            ANALISTA.query.filter().join(
                TIME.query.filter_by(GESTOR_ID=user_id))).count()
        servico_fechado = SOL_SERVICO.query.filter(
            SOL_SERVICO.STATUS.in_(['FINALIZADA', 'NÃO APROVADO'])).join(
            ANALISTA.query.filter().join(
                TIME.query.filter_by(GESTOR_ID=user_id))).count()
        import_aberto = SOL_IMPORT.query.filter(
            SOL_IMPORT.STATUS.notin_(['FINALIZADA', 'NÃO APROVADO'])).join(
            ANALISTA.query.filter().join(
                TIME.query.filter_by(GESTOR_ID=user_id))).count()
        import_fechado = SOL_IMPORT.query.filter(
            SOL_IMPORT.STATUS.in_(['FINALIZADA', 'NÃO APROVADO'])).join(
            ANALISTA.query.filter().join(
                TIME.query.filter_by(GESTOR_ID=user_id))).count()
        share_aberto = SOL_SHARE.query.filter(
            SOL_SHARE.STATUS.notin_(['FINALIZADA', 'NÃO APROVADO'])).join(
            ANALISTA.query.filter().join(
                TIME.query.filter_by(GESTOR_ID=user_id))).count()
        share_fechado = SOL_SHARE.query.filter(
            SOL_SHARE.STATUS.in_(['FINALIZADA', 'NÃO APROVADO'])).join(
            ANALISTA.query.filter().join(
                TIME.query.filter_by(GESTOR_ID=user_id))).count()
        ticket_aberto = SOL_TICKET.query.filter(
            SOL_TICKET.STATUS.notin_(['FINALIZADA', 'NÃO APROVADO'])).join(
            ANALISTA.query.filter().join(
                TIME.query.filter_by(GESTOR_ID=user_id))).count()
        ticket_fechado = SOL_TICKET.query.filter(
            SOL_TICKET.STATUS.in_(['FINALIZADA', 'NÃO APROVADO'])).join(
            ANALISTA.query.filter().join(
                TIME.query.filter_by(GESTOR_ID=user_id))).count()
        issue_interna_aberto = SOL_ISSUE_INT.query.filter(
            SOL_ISSUE_INT.STATUS.notin_(['FINALIZADA', 'NÃO APROVADO'])).join(
            ANALISTA.query.filter().join(
                TIME.query.filter_by(GESTOR_ID=user_id))).count()
        issue_interna_fechado = SOL_ISSUE_INT.query.filter(
            SOL_ISSUE_INT.STATUS.in_(['FINALIZADA', 'NÃO APROVADO'])).join(
            ANALISTA.query.filter().join(
                TIME.query.filter_by(GESTOR_ID=user_id))).count()
        help_aberto = HELP.query.filter(
            HELP.STATUS.notin_(['FINALIZADA', 'CANCELADO'])).join(
            ANALISTA.query.filter().join(
                TIME.query.filter_by(GESTOR_ID=user_id))).count()
        help_fechado = HELP.query.filter(
            HELP.STATUS.in_(['FINALIZADA', 'CANCELADO'])).join(
            ANALISTA.query.filter().join(
                TIME.query.filter_by(GESTOR_ID=user_id))).count()
    elif user_type== 'H':
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
    elif user_type== 'A':
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
        tps = CONTROLE_TPS_ANALISTAS.query.filter_by(
            ANALISTA=user_email.split('@')[0].replace('.', ' ').title()).all()

        result = {}

        for tp in tps:
            result[f'cod_int{tp.id}'] = {
                "NRO_TP": tp.NRO_TP,
                "ISSUE": tp.ISSUE,
                "ANALISTA": tp.ANALISTA.strip(),
                "GRUPO": tp.GRUPO.strip(),
                "RESUMO": tp.RESUMO.strip(),
                "DIAS_ABERTO": tp.DIAS_ABERTO,
                "DTA_FIM": tp.DTA_FIM,
                "DTA_ULT_MOV": tp.DTA_ULT_MOV,
                "STATUS": tp.STATUS.strip(),
                "PRIORIDADE": tp.PRIORIDADE
            }

        result = {"Lista": result}

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

        analistas = ANALISTA.query.filter(
            ANALISTA.TIME_ID.in_(lista_times)).all()
        lista_analistas = []
        for i in analistas:
            lista_analistas.append(i.EMAIL.split(
                '@')[0].replace('.', ' ').title())

        tps = CONTROLE_TPS_ANALISTAS.query.filter(
            CONTROLE_TPS_ANALISTAS.ANALISTA.in_(lista_analistas)).all()

        result = {}

        for tp in tps:
            aux = tp.ANALISTA.strip().replace(' ', '.').lower() + '@linx.com.br'
            analista = ANALISTA.query.filter_by(EMAIL=aux).first()
            time = TIME.query.filter_by(id=analista.TIME_ID).first()

            result[f'cod_int{tp.id}'] = {
                "NRO_TP": tp.NRO_TP,
                "ISSUE": tp.ISSUE,
                "ANALISTA": tp.ANALISTA.strip(),
                "TIME": time.NOME,
                "GRUPO": tp.GRUPO.strip(),
                "RESUMO": tp.RESUMO.strip(),
                "DIAS_ABERTO": tp.DIAS_ABERTO,
                "DTA_FIM": tp.DTA_FIM,
                "DTA_ULT_MOV": tp.DTA_ULT_MOV,
                "STATUS": tp.STATUS.strip(),
                "PRIORIDADE": tp.PRIORIDADE
            }

        return result

    return result


def busca_inf_filas_gerais():
    info_tps = CONTROLE_TPS_GERAIS.query.first()

    result = jsonify(
        {   "id": "1",
            "name": "Apollo",
            "P0": info_tps.APOLLO_p0,
            "P1": info_tps.APOLLO_p1,
            "P2": info_tps.APOLLO_p2,
            "P3": info_tps.APOLLO_p3,
            "qtd_tp": info_tps.APOLLO_tot
        },
        {   "id": "2",
            "name": "Bravos",
            "P0": info_tps.BRAVOS_p0,
            "P1": info_tps.BRAVOS_p1,
            "P2": info_tps.BRAVOS_p2,
            "P3": info_tps.BRAVOS_p3,
            "qtd_tp": info_tps.BRAVOS_tot
        },
        {   "id": "3",
            "name": "Toyota",
            "P0": info_tps.TOYOTA_p0,
            "P1": info_tps.TOYOTA_p1,
            "P2": info_tps.TOYOTA_p2,
            "P3": info_tps.TOYOTA_p3,
            "qtd_tp": info_tps.TOYOTA_tot
        },
        {   "id": "4",
            "name": "Autoshop",
            "P0": info_tps.AUTOSHOP_p0,
            "P1": info_tps.AUTOSHOP_p1,
            "P2": info_tps.AUTOSHOP_p2,
            "P3": info_tps.AUTOSHOP_p3,
            "qtd_tp": info_tps.AUTOSHOP_tot
        },
        {   "id": "5",
            "name": "Berçário",
            "P0": info_tps.BERCARIO_p0,
            "P1": info_tps.BERCARIO_p1,
            "P2": info_tps.BERCARIO_p2,
            "P3": info_tps.BERCARIO_p3,
            "qtd_tp": info_tps.BERCARIO_tot
        },
        {   "id": "6",
            "name": "Financeiro",
            "P0": info_tps.FINANCEIRO_p0,
            "P1": info_tps.FINANCEIRO_p1,
            "P2": info_tps.FINANCEIRO_p2,
            "P3": info_tps.FINANCEIRO_p3,
            "qtd_tp": info_tps.FINANCEIRO_tot
        },
        {   "id": "7",
            "name": "NFSE/NFCE",
            "P0": info_tps.NFCE_p0,
            "P1": info_tps.NFCE_p1,
            "P2": info_tps.NFCE_p2,
            "P3": info_tps.NFCE_p3,
            "qtd_tp": info_tps.NFCE_tot
        },
        {   "id": "8",
            "name": "Montadoras",
            "P0": info_tps.MONTADORA_p0,
            "P1": info_tps.MONTADORA_p1,
            "P2": info_tps.MONTADORA_p2,
            "P3": info_tps.MONTADORA_p3,
            "qtd_tp": info_tps.MONTADORA_tot
        },
        {   "id": "9",
            "name": "Mobile",
            "P0": info_tps.MOBILE_p0,
            "P1": info_tps.MOBILE_p1,
            "P2": info_tps.MOBILE_p2,
            "P3": info_tps.MOBILE_p3,
            "qtd_tp": info_tps.MOBILE_tot
        },
        {   "id": "10",
            "name": "Contábil/Fiscal",
            "P0": info_tps.CONTABIL_p0,
            "P1": info_tps.CONTABIL_p1,
            "P2": info_tps.CONTABIL_p2,
            "P3": info_tps.CONTABIL_p3,
            "qtd_tp": info_tps.CONTABIL_tot
        },
        {   "id": "11",
            "name": "CC1",
            "P0": info_tps.CC1_p0,
            "P1": info_tps.CC1_p1,
            "P2": info_tps.CC1_p2,
            "P3": info_tps.CC1_p3,
            "qtd_tp": info_tps.CC1_tot
        }
    )

    return result


def busca_inf_bases():
    bases = BASES.query.all()

    result = {}

    for i in bases:

        result[f'cod_int{i.id}'] = {
            "Cliente": i.CLIENTE,
            "Charset": i.CHARSET,
            "Servidor": i.SERVIDOR,
            "Estrutura": i.ESTRUTURA,
            "Instancia": i.INSTANCIA,
            "Usuario": i.USUARIO,
            "Marca": i.MARCA,
            "Tamanho": i.TAMANHO
        }

    return result


def busca_inf_filas_analitic(user_id, user_type):
    data_atual = date.today()
    last_date = str(data_atual.replace(day=1) + timedelta(monthrange(data_atual.year, data_atual.month)[1] - 1))
    first_date = str(data_atual.replace(day=1))

    dt2 = data_atual.replace(day=1) + timedelta(monthrange(data_atual.year, data_atual.month)[1])
    dt1 = data_atual.replace(day=1)

    dias_uteis = workdays.networkdays(dt1, dt2)

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

        analistas = ANALISTA.query.filter(
            ANALISTA.TIME_ID.in_(lista_times)).all()
            
        lista_analistas = []
        
        for i in analistas:
            lista_analistas.append(i.EMAIL.split(
                '@')[0].upper())
            
        lista_analistas = r"', '".join(map(str,lista_analistas))

    
    attempts = 5
    result_database = ""

    while attempts:
        try:
            result_database = database_azure.execute(f"""SELECT ENCERRADOS.no_responsavel,
            CONTROLE_FILAS.GERAL,
            CONTROLE_FILAS.ISSUE,
            CONTROLE_FILAS.MAIS_15,
            CONTROLE_FILAS.BACKLOG,
            cast(ENCERRADOS.qtd_encerrados AS NUMERIC(9))  AS ATINGIMENTO,
	   format(round((coalesce(cast(REABERTOS.QTD_REABERTURAS as numeric(9)), 0) /
				coalesce(cast(ENCERRADOS.QTD_ENCERRADOS as numeric(9)), 0)) * 100, 2) , '0.00') as PERC_REABERTOS,
	   format(Round((coalesce(Cast(ENCERRADOS_DENTRO_SLA.qtd_encerrados_dentro_sla as numeric(9)), 1) / 
			coalesce(Cast(ENCERRADOS.qtd_encerrados as numeric(9)), 0) ) * 100, 2), '#.00') as SLA,
	   format(Round((
			coalesce(Cast(PESQUISAS_RESPONDIDAS.qtd_pesquisas_respondidas as numeric(9)), 0) / 
			coalesce(Cast(ENCERRADOS.qtd_encerrados as numeric(9)), 0) ) * 100, 2), '0.00') as PERC_RESPOSTA,   
	   format(round(((coalesce(cast(PESQUISAS_PROMOTORAS.QTD_PESQUISAS_PROMOTORAS as numeric(9)), 1) - 
			coalesce(cast(PESQUISAS_DETRATORAS.QTD_PESQUISAS_DETRATORAS as numeric(9)),0)) /
			coalesce(cast(PESQUISAS_RESPONDIDAS.QTD_PESQUISAS_RESPONDIDAS as numeric(9)), 1)) * 100, 2), '#.00') as NPS
        from (select count(*) QTD_ENCERRADOS, no_responsavel
            from chamado_new
                where  segmento = 'AUTOMOTIVO'
                and no_responsavel in ('{lista_analistas}')
                and dh_conclusao between cast('{first_date} 00:00:00' AS DATETIME)
                and cast('{last_date} 23:59:59' AS DATETIME)
                and id_tarefa > 0
            GROUP  BY no_responsavel) ENCERRADOS
        left outer join (SELECT Count(*) QTD_ENCERRADOS_DENTRO_SLA, no_responsavel
            FROM chamado_new
                WHERE  segmento = 'AUTOMOTIVO'
                and no_responsavel in ('{lista_analistas}')
                AND dh_conclusao between cast('{first_date} 00:00:00' AS DATETIME)
                and cast('{last_date} 23:59:59' AS DATETIME)
                AND id_tarefa > 0
                AND dh_conclusao <= dh_fim_previsto
            GROUP  BY no_responsavel) ENCERRADOS_DENTRO_SLA
        ON ( ENCERRADOS.no_responsavel = ENCERRADOS_DENTRO_SLA.no_responsavel )
        LEFT OUTER JOIN (SELECT Count(*) QTD_ENCERRADOS_FORA_SLA, no_responsavel
            FROM chamado_new
                WHERE  segmento = 'AUTOMOTIVO'
                and no_responsavel in ('{lista_analistas}')
                AND dh_conclusao between cast('{first_date} 00:00:00' AS DATETIME)
                and cast('{last_date} 23:59:59' AS DATETIME)
                AND id_tarefa > 0
                AND dh_conclusao > dh_fim_previsto
            GROUP  BY no_responsavel) ENCERRADOS_FORA_SLA
        ON ( ENCERRADOS.no_responsavel = ENCERRADOS_FORA_SLA.no_responsavel )
        LEFT OUTER JOIN (SELECT Count(*) QTD_PESQUISAS_RESPONDIDAS, no_responsavel
            FROM   chamado_new
                WHERE  segmento = 'AUTOMOTIVO'
                and no_responsavel in ('{lista_analistas}')
                AND dh_conclusao between cast('{first_date} 00:00:00' AS DATETIME)
                and cast('{last_date} 23:59:59' AS DATETIME)
                AND id_tarefa > 0
                AND dh_resp_pesquisa IS NOT NULL
            GROUP  BY no_responsavel) PESQUISAS_RESPONDIDAS
        ON ( ENCERRADOS.no_responsavel = PESQUISAS_RESPONDIDAS.no_responsavel )
        LEFT OUTER JOIN (SELECT Count(*) QTD_PESQUISAS_PROMOTORAS, no_responsavel
            FROM chamado_new
                WHERE segmento = 'AUTOMOTIVO'
                and no_responsavel in ('{lista_analistas}')
                AND dh_conclusao between cast('{first_date} 00:00:00' AS DATETIME)
                and cast('{last_date} 23:59:59' AS DATETIME)
                AND id_tarefa > 0
                AND dh_resp_pesquisa IS NOT NULL
                AND nu_resp_geral IN ( 9, 10 )
            GROUP  BY no_responsavel) PESQUISAS_PROMOTORAS
        ON ( ENCERRADOS.no_responsavel = PESQUISAS_PROMOTORAS.no_responsavel )
        LEFT OUTER JOIN (SELECT Count(*) QTD_PESQUISAS_NEUTRAS, no_responsavel
            FROM chamado_new
                WHERE segmento = 'AUTOMOTIVO'
                and no_responsavel in ('{lista_analistas}')
                AND dh_conclusao between cast('{first_date} 00:00:00' AS DATETIME)
                and cast('{last_date} 23:59:59' AS DATETIME)
                AND id_tarefa > 0
                AND dh_resp_pesquisa IS NOT NULL
                AND nu_resp_geral IN ( 7, 8 )
            GROUP  BY no_responsavel) PESQUISAS_NEUTRAS
        ON ( ENCERRADOS.no_responsavel = PESQUISAS_NEUTRAS.no_responsavel )
        LEFT OUTER JOIN (SELECT Count(*) QTD_PESQUISAS_DETRATORAS, no_responsavel
        FROM chamado_new
            WHERE segmento = 'AUTOMOTIVO'
                and no_responsavel in ('{lista_analistas}')
                AND dh_conclusao between cast('{first_date} 00:00:00' AS DATETIME)
                and cast('{last_date} 23:59:59' AS DATETIME)
                AND id_tarefa > 0
                AND dh_resp_pesquisa IS NOT NULL
                AND nu_resp_geral <= 6
            GROUP  BY no_responsavel) PESQUISAS_DETRATORAS
        ON ( ENCERRADOS.no_responsavel = PESQUISAS_DETRATORAS.no_responsavel)
        left outer join (select sum(NU_REABERTURA) QTD_REABERTURAS, NO_RESPONSAVEL
            from CHAMADO_NEW
                where SEGMENTO = 'AUTOMOTIVO'
                and no_responsavel in ('{lista_analistas}')
                AND dh_conclusao between cast('{first_date} 00:00:00' AS DATETIME)
                and cast('{last_date} 23:59:59' AS DATETIME)
                and ID_TAREFA > 0
                and NU_REABERTURA > 0
            group by NO_RESPONSAVEL) REABERTOS
        on (ENCERRADOS.NO_RESPONSAVEL = REABERTOS.NO_RESPONSAVEL)
        left outer join (select CN.NO_RESPONSAVEL, 
        (select count(*) from CHAMADO_NEW 
            where NO_RESPONSAVEL = CN.NO_RESPONSAVEL 
            and ABERTO = 'SIM' 
            and SEGMENTO = 'AUTOMOTIVO') as GERAL, 
        (select count(*) from CHAMADO_NEW  
            where NO_RESPONSAVEL = CN.NO_RESPONSAVEL 
            and ABERTO = 'SIM' 
            and ID_ISSUE is not null and 
            SEGMENTO = 'AUTOMOTIVO') as ISSUE, 
        (select count(*) from CHAMADO_NEW 
            where NO_RESPONSAVEL = CN.NO_RESPONSAVEL 
            and ABERTO = 'SIM' 
            and datediff(day, DH_ABERTURA, getdate()) > 14 
            and SEGMENTO = 'AUTOMOTIVO') as MAIS_15, 
        (select count(*) from CHAMADO_NEW  
            where NO_RESPONSAVEL = CN.NO_RESPONSAVEL 
            and ABERTO = 'SIM' 
            and DH_FIM_PREVISTO < getdate() 
            and SEGMENTO = 'AUTOMOTIVO') as BACKLOG
        from CHAMADO_NEW CN
        where CN.NO_RESPONSAVEL in ('{lista_analistas}') 
        group by CN.NO_RESPONSAVEL) CONTROLE_FILAS
        ON ( ENCERRADOS.no_responsavel = CONTROLE_FILAS.NO_RESPONSAVEL);""").fetchall()
            break
        except Exception:
            attempts -= 1
        
    if not result_database: 
        return {"message": "O banco de dados do wf demorou demais para responder."}, 406
    
    result = []
    for value in result_database:
        aux = value[0] + '@linx.com.br'
        analista = ANALISTA.query.filter_by(EMAIL=aux).first()
        time = TIME.query.filter_by(id=analista.TIME_ID).first()

        atingimento = str(100 * (value[5] / (dias_uteis * analista.META)))[:5]

        result.append({
            "analista": value[0],
            "time": time.NOME,
            "qtdFila": value[1],
            "qtdIssue": value[2],
            "qtdMais": value[3],
            "qtdBacklog": value[4],
            "ating": atingimento, 
            "abert": value[6], 
            "sla": value[7], 
            "res": value[8],
            "nps": value[9],
        })
        

    return result

def request_bug_create(user_id, what, how, obs, req_type):
    new_request = REQUEST_BUG(SOLICITANTE=user_id, OQUE=what, COMO=how, OBS=obs, TIPO=req_type, STATUS='NÃO INICIADO')

    database.session.add(new_request)
    database.session.commit()

    return {'message': 'Solicitação enviada com sucesso, agradecemos sua colaboração!'}, 200