import logging
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from .models import Colaborador, Atendimento
from .services import WppConnectService 
from .constants import MENU_INICIAL, SETORES, MSG_AGUARDANDO_DETALHES, MSG_ENCAMINHADO, MSG_ERRO_GENERICO

logger = logging.getLogger(__name__)

# 🔒 CONFIGURAÇÃO DE SEGURANÇA (WHITELIST)
# Adicione aqui todos os IDs que podem falar com o bot
NUMEROS_PERMITIDOS = [
    "5592985621293@c.us",   # Seu Celular Principal (com o 9 dígito)
    "559285621293@c.us",    # Seu Celular (formato antigo sem o 9, por garantia)
    "147176365772893@lid",  # 📱 Seu Tablet SI-03 (Identificado nos logs)
]

class WebhookView(APIView):
    def post(self, request):
        try:
            data = json.loads(request.body)
        except:
            return Response(status=status.HTTP_200_OK)

        # 1. Normaliza o Evento
        event = str(data.get('event', '')).lower()
        
        # Só nos interessa se for mensagem
        if 'onmessage' in event:
            print(f"\n📩 PROCESSANDO MENSAGEM (Evento: {event})")

            # 2. Estratégia de Busca Inteligente
            payload = data.get('data') if 'data' in data and isinstance(data['data'], dict) else data

            # 3. Extração dos Campos
            sender = payload.get('from')
            body = payload.get('body')
            is_group = payload.get('isGroup', False)
            from_me = payload.get('fromMe', False)
            notify_name = payload.get('notifyName', 'Cliente')

            print(f"   👤 De: {notify_name} ({sender})")
            
            # 4. Filtros de Segurança
            
            # A. Ignora mensagens enviadas por mim mesmo
            if from_me:
                print("   🚫 Ignorando mensagem enviada por mim.")
                return Response(status=status.HTTP_200_OK)
            
            # B. Ignora Grupos
            if is_group:
                print("   🚫 Ignorando mensagem de grupo.")
                return Response(status=status.HTTP_200_OK)

            # C. 🔒 WHITELIST (O Porteiro)
            # Verifica se o remetente está na lista de permitidos
            if sender not in NUMEROS_PERMITIDOS:
                print(f"   🔒 BLOQUEADO: O número {sender} não está na lista de permitidos.")
                # DICA: Se quiser desbloquear temporariamente para testes, comente as duas linhas abaixo
                return Response(status=status.HTTP_200_OK)

            # -------------------------------

            if not body or not sender:
                print("   ⚠️ Dados incompletos, ignorando.")
                return Response(status=status.HTTP_200_OK)

            # 5. LÓGICA DO BOT (MÁQUINA DE ESTADOS)
            print("   ✅ Mensagem Autorizada! Iniciando lógica de atendimento...")
            
            try:
                # A. Identifica/Cria Colaborador
                # Usa o notifyName se o nome não existir, senão mantém o antigo
                colaborador, created = Colaborador.objects.get_or_create(
                    telefone=sender,
                    defaults={'nome': notify_name}
                )
                
                # Se for um ID estranho (tablet), tenta atualizar o nome se estiver genérico
                if not created and colaborador.nome == 'Cliente' and notify_name != 'Cliente':
                    colaborador.nome = notify_name
                    colaborador.save()

                # B. Busca Atendimento Aberto
                atendimento = Atendimento.objects.filter(
                    colaborador=colaborador
                ).exclude(estagio='FINALIZADO').first()

                # C. Cria Novo se não existir
                if not atendimento:
                    atendimento = Atendimento.objects.create(
                        colaborador=colaborador,
                        estagio='INICIO'
                    )
                    print("   🆕 Novo atendimento iniciado.")

                # D. Processa a Resposta
                client = WppConnectService()
                texto_limpo = str(body).strip()

                # --- LÓGICA DOS MENUS ---
                
                if atendimento.estagio == 'INICIO':
                    print("   🤖 Enviando Menu Inicial...")
                    client.enviar_texto(sender, MENU_INICIAL)
                    atendimento.estagio = 'MENU_PRINCIPAL'
                    atendimento.save()

                elif atendimento.estagio == 'MENU_PRINCIPAL':
                    print(f"   🤖 Processando escolha: {texto_limpo}")
                    if texto_limpo in SETORES:
                        setor_info = SETORES[texto_limpo]
                        atendimento.setor_escolhido = texto_limpo
                        atendimento.estagio = 'AGUARDANDO_DETALHES'
                        atendimento.save()
                        client.enviar_texto(sender, MSG_AGUARDANDO_DETALHES.format(setor=setor_info['nome']))
                    else:
                        client.enviar_texto(sender, MSG_ERRO_GENERICO)

                elif atendimento.estagio == 'AGUARDANDO_DETALHES':
                    print("   🤖 Encaminhando chamado...")
                    setor_id = atendimento.setor_escolhido
                    setor_info = SETORES.get(setor_id)
                    
                    # Gera Protocolo
                    protocolo = f"NT-{atendimento.id}"
                    
                    # Responde ao Usuário
                    msg_final = MSG_ENCAMINHADO.format(
                        setor=setor_info['nome'] if setor_info else 'Geral', 
                        protocolo=protocolo
                    )
                    client.enviar_texto(sender, msg_final)
                    
                    # (Opcional) Envio para grupo do setor
                    # client.enviar_para_grupo(setor_info['grupo_id'], "Nova solicitação...")

                    atendimento.estagio = 'FINALIZADO'
                    atendimento.protocolo = protocolo
                    atendimento.save()
                    print(f"   🏁 Atendimento Finalizado: {protocolo}")

            except Exception as e:
                print(f"❌ Erro na lógica do bot: {e}")
                logger.error(e)

        return Response(status=status.HTTP_200_OK)

# --- VIEW DO DASHBOARD ---
def dashboard_home(request):
    # Pega os atendimentos ordenados por data (mais recente primeiro)
    atendimentos = Atendimento.objects.select_related('colaborador').all().order_by('-data_inicio')
    
    return render(request, 'dashboard/home.html', {
        'atendimentos': atendimentos
    })