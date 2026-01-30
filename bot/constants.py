# Mapeamento do Menu Principal
MENU_INICIAL = """
Olá, bem-vindo à *Norte Tech*! 🤖
Sou seu assistente virtual de triagem.

Por favor, selecione o departamento desejado:

*1.* 💻 TI / Suporte
*2.* 👥 Recursos Humanos (RH)
*3.* 🚗 Frota / Transporte
*4.* 💰 Financeiro
*5.* 🏗️ Manutenção Predial
*6.* 🧹 Limpeza / Conservação

_Responda apenas com o número da opção._
"""

# Configuração dos Setores (Nome e ID do Grupo de Destino)
# IMPORTANTE: Você precisará substituir os IDs abaixo pelos JIDs reais dos grupos (ex: 12036... @g.us)
SETORES = {
    '1': {
        'nome': 'TI / Suporte',
        'grupo_id': '120363123456789@g.us'  # <--- COLOCAR ID REAL DO GRUPO DE TI
    },
    '2': {
        'nome': 'Recursos Humanos',
        'grupo_id': 'grupo_rh_id_aqui'
    },
    '3': {
        'nome': 'Frota',
        'grupo_id': 'grupo_frota_id_aqui'
    },
    '4': {
        'nome': 'Financeiro',
        'grupo_id': 'grupo_financeiro_id_aqui'
    },
    '5': {
        'nome': 'Manutenção',
        'grupo_id': 'grupo_manutencao_id_aqui'
    },
    '6': {
        'nome': 'Limpeza',
        'grupo_id': 'grupo_limpeza_id_aqui'
    }
}

# Mensagens Padronizadas
MSG_AGUARDANDO_DETALHES = """
Certo, você selecionou *{setor}*.

Por favor, descreva sua solicitação em uma única mensagem para eu encaminhar ao responsável.
"""

MSG_ENCAMINHADO = """
✅ *Solicitação Recebida!*

Sua demanda foi encaminhada para a equipe de *{setor}*.
Protocolo: *{protocolo}*

Em breve alguém entrará em contato. Obrigado!
"""

MSG_ERRO_GENERICO = "Desculpe, não entendi. Digite apenas o número da opção desejada."