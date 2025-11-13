# Em app/gateways/dialogflow_gateway.py
import os
from google.cloud import dialogflow_v2 as dialogflow
from app.core.settings import settings

def detectar_intencao(user_id: str, texto: str, lang: str = "pt-BR") -> dict:
    """
    Envia o texto para o Dialogflow e retorna um dicionário
    com a resposta e os parâmetros.
    """
    
    session_client = dialogflow.SessionsClient()
    session_path = session_client.session_path(settings.PROJECT_ID, user_id)
    text_input = dialogflow.TextInput(text=texto, language_code=lang)
    query_input = dialogflow.QueryInput(text=text_input)

    try:
        response = session_client.detect_intent(
            request={"session": session_path, "query_input": query_input}
        )
        
        query_result = response.query_result
        
        # Convertendo o objeto 'MapComposite' para um dict Python simples
        parametros = dict(query_result.parameters)
        
        return {
            "texto_resposta": query_result.fulfillment_text,
            "intencao": query_result.intent.display_name,
            "parametros": parametros,
        }

    except Exception as e:
        print(f"Erro ao conectar com Dialogflow: {e}")
        return {
            "texto_resposta": "Desculpe, não consegui processar sua mensagem agora.",
            "intencao": "Erro",
            "parametros": {},
        }