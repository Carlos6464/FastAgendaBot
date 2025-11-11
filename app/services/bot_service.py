# Em app/services/bot_service.py
from app.schemas import BotMessageIn, BotMessageOut
from app.gateways import dialogflow_gateway
from app.gateways import google_calendar_gateway # Já importamos o módulo
from datetime import timedelta, datetime
from dateutil.parser import isoparse

async def processar_mensagem(mensagem: BotMessageIn) -> BotMessageOut:
    
    print(f"Mensagem recebida do usuário {mensagem.user_id}: {mensagem.text}")

    resposta_ia = dialogflow_gateway.detectar_intencao(
        user_id=mensagem.user_id,
        texto=mensagem.text
    )
    
    print(f"Resposta do Dialogflow: {resposta_ia}")
    
    params = resposta_ia["parametros"]
    intencao = resposta_ia["intencao"]

    # Verificamos se temos TUDO que precisamos
    if (
        intencao == "AgendarHorario" and 
        params.get("date") and 
        params.get("time")
    ):
        
        date_str = params.get("date")
        time_str = params.get("time")
        
        print(f">>> HORA DE AGENDAR! Data suja: {date_str}, Hora suja: {time_str}")
        
        try:
            # 1. Parseamos ambas as datas
            parsed_date = isoparse(date_str)
            parsed_time = isoparse(time_str)
            
            # 2. Criamos o datetime final "limpo"
            start_time = parsed_date.replace(
                hour=parsed_time.hour,
                minute=parsed_time.minute,
                second=parsed_time.second,
                microsecond=0
            )
            
            # 3. Definimos a duração (ex: 1 hora)
            end_time = start_time + timedelta(hours=1)
            
            # --- 4. A NOVA LÓGICA DE VERIFICAÇÃO ---
            
            esta_livre = google_calendar_gateway.verificar_disponibilidade_agenda(
                start_time=start_time,
                end_time=end_time
            )
            
            if esta_livre:
                # 5. Se ESTIVER LIVRE, criamos o evento
                evento_criado = google_calendar_gateway.criar_evento_google_calendar(
                    titulo="Agendamento - Cliente do Bot",
                    start_time=start_time,
                    end_time=end_time
                )
                
                if evento_criado:
                    link_evento = evento_criado.get('htmlLink')
                    data_formatada = start_time.strftime('%d/%m/%Y às %H:%M')
                    texto_final = f"Agendamento confirmado! ✅\nHorário: {data_formatada}\n\nVocê pode ver seu evento aqui: {link_evento}"
                else:
                    texto_final = "Consegui entender seu horário, mas falhei ao tentar agendar no sistema. Tente novamente mais tarde."
            else:
                # 6. Se ESTIVER OCUPADO, informamos o usuário
                data_formatada = start_time.strftime('%d/%m/%Y às %H:%M')
                texto_final = f"Desculpe, o horário de {data_formatada} já está OCUPADO. 😕\n\nPor favor, tente outro dia ou horário."

        except Exception as e:
            print(f"Erro ao processar data ou criar evento: {e}")
            texto_final = "Humm, algo deu errado com a data que você me passou. Vamos tentar de novo?"
        
        return BotMessageOut(
            user_id=mensagem.user_id,
            response_text=texto_final
        )

    # Se não for, apenas devolvemos a resposta normal do Dialogflow
    return BotMessageOut(
        user_id=mensagem.user_id,
        response_text=resposta_ia["texto_resposta"]
    )