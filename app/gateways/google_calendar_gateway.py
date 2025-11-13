# Em app/gateways/google_calendar_gateway.py
import datetime
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from app.core.settings import settings

# Definimos as "permissões" que nossa credencial (do .json) pedirá
SCOPES = ['https://www.googleapis.com/auth/calendar']

def criar_evento_google_calendar(
    titulo: str, 
    start_time: datetime.datetime, 
    end_time: datetime.datetime
) -> dict:
    """
    Cria um evento na agenda do bot e retorna o link do evento.
    """
    
    try:
        # 1. Carrega as credenciais do nosso .json (o caminho está no settings)
        creds = Credentials.from_service_account_file(
            settings.GOOGLE_APPLICATION_CREDENTIALS, scopes=SCOPES
        )
        
        # 2. Constrói o "cliente" da API
        service = build('calendar', 'v3', credentials=creds)
        
        # 3. Monta o corpo (body) do evento
        event = {
            'summary': titulo,
            'description': 'Evento agendado automaticamente pelo FastAgendaBot',
            'start': {
                'dateTime': start_time.isoformat(),
                'timeZone': 'America/Sao_Paulo',
            },
            'end': {
                'dateTime': end_time.isoformat(),
                'timeZone': 'America/Sao_Paulo',
            },
        }

        # 4. Chama a API para inserir o evento
        print(f"Enviando para o Calendar ID: {settings.CALENDAR_ID}")
        event_result = service.events().insert(
            calendarId=settings.CALENDAR_ID, 
            body=event
        ).execute()
        
        print(f"Evento criado com sucesso: {event_result.get('htmlLink')}")
        
        # 5. Retorna o evento criado (especialmente o link)
        return event_result
        
    except Exception as e:
        print(f"Erro ao criar evento no Google Calendar: {e}")
        return None
    

def verificar_disponibilidade_agenda(
        start_time: datetime.datetime, 
        end_time: datetime.datetime
    ) -> bool:
        """
        Verifica se já existe algum evento no calendário no intervalo de tempo solicitado.
        Retorna True se estiver LIVRE, False se estiver OCUPADO.
        """
        
        try:
            creds = Credentials.from_service_account_file(
                settings.GOOGLE_APPLICATION_CREDENTIALS, scopes=SCOPES
            )
            service = build('calendar', 'v3', credentials=creds)
            
            # Formata as datas para o padrão da API (ISO 8601)
            time_min_iso = start_time.isoformat()
            time_max_iso = end_time.isoformat()

            print(f"Verificando disponibilidade de {time_min_iso} até {time_max_iso}")

            events_result = service.events().list(
                calendarId=settings.CALENDAR_ID,
                timeMin=time_min_iso,
                timeMax=time_max_iso,
                maxResults=1,
                singleEvents=True
            ).execute()
            
            events = events_result.get('items', [])

            if not events:
                print(">>> Horário LIVRE.")
                return True  # Livre!
            
            print(f">>> Horário OCUPADO. Encontrado: {events[0]['summary']}")
            return False # Ocupado!

        except Exception as e:
            print(f"Erro ao VERIFICAR disponibilidade: {e}")
            return False