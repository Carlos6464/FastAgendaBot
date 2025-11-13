# Em app/core/settings.py
import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Encontramos o caminho para o arquivo .env
# Isso garante que ele funcione, não importa de onde você rode o script.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
env_path = os.path.join(BASE_DIR, '.env')

# Carregamos o .env no ambiente do sistema (os.environ)
# Agora, a biblioteca do Google encontrará a variável!
load_dotenv(dotenv_path=env_path)

# Agora a classe Settings vai ler as variáveis que o load_dotenv
# acabou de colocar no ambiente.
class Settings(BaseSettings):
    PROJECT_ID: str
    GOOGLE_APPLICATION_CREDENTIALS: str
    CALENDAR_ID: str
    TELEGRAM_TOKEN: str
    
# Criamos a instância única que será usada em todo o app.
settings = Settings()