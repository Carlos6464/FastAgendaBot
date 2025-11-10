# FastAgenda Bot 🤖

Backend (API) para um chatbot de agendamento, construído com FastAPI. Este projeto serve como um MVP (Produto Mínimo Viável) para um serviço de agendamento automatizado, utilizando uma arquitetura limpa (C-S-R) e integração com o Google Dialogflow para processamento de linguagem natural.

## 🚀 Tecnologias Utilizadas

* **Python 3.10+**
* **FastAPI** : Para a criação da API de alta performance.
* **Uvicorn** : Como servidor ASGI para rodar a aplicação.
* **Pydantic** : Para validação de dados e schemas (usado nativamente pelo FastAPI).
* **(Futuro) Google Dialogflow ES** : Para o "cérebro" (NLP) do bot.
* **(Futuro) Google Calendar API** : Para gerenciar os agendamentos.

## 🏛️ Estrutura do Projeto (Arquitetura C-S-R)

O projeto segue uma variação da Arquitetura em Camadas, focada em separação de responsabilidades:

* **`main.py`** : Ponto de entrada da aplicação. Responsável por iniciar o FastAPI e incluir os módulos de rotas.
* **`app/`** : Contém toda a lógica principal da aplicação.
* **`app/routers/` (Controllers)** : A camada de "Controller". Recebe as requisições HTTP, valida os dados de entrada (usando `schemas`) e chama os `services` apropriados.
* **`app/services/` (Services)** : A camada de "Serviço". Contém toda a lógica de negócio (ex: "processar mensagem do bot", "encontrar horário vago"). Orquestra os `gateways` e `repositories`.
* **`app/repositories/` (Repositories)** : Camada de acesso a dados. Responsável por toda a comunicação com o banco de dados (ex: salvar um agendamento).
* **`app/gateways/` (Gateways)** : Camada de comunicação com APIs externas. Abstrai a lógica de chamada a serviços como Google Dialogflow ou Google Calendar.
* **`app/schemas.py`** : Contém os modelos Pydantic (schemas) que definem as estruturas de dados de entrada e saída da API.

## 🛠️ Configuração e Instalação

Siga os passos abaixo para rodar o projeto localmente.

### 1. Pré-requisitos

* Python 3.10 ou superior
* Uma conta Google Cloud com o Dialogflow ES ativado.

### 2. Instalação

1. Clone este repositório:
   **Bash**

   ```
   git clone https://[SEU-LINK-GIT]/fastagenda.git
   cd fastagenda
   ```
2. Crie e ative um ambiente virtual:
   **Bash**

   ```
   python -m venv venv
   ```

   * *No Windows:* `.\venv\Scripts\activate`
   * *No macOS/Linux:* `source venv/bin/activate`
3. Instale as dependências:
   **Bash**

   ```
   pip install -r requirements.txt
   ```

### 3. Configuração de Credenciais

1. Acesse seu projeto no Google Cloud Console e navegue para "IAM e Admin" > "Contas de Serviço".
2. Encontre a conta de serviço associada ao seu agente do Dialogflow.
3. Crie uma nova chave (JSON) e faça o download.
4. Renomeie o arquivo para `fastagenda-credentials.json` e coloque-o na **pasta raiz** do projeto.
   **⚠️ IMPORTANTE** : Este arquivo **NÃO DEVE** ser enviado para o Git. Ele já está incluído no `.gitignore`.

## 🏃 Como Executar

Com o ambiente virtual ativado, rode o servidor Uvicorn:

**Bash**

```
uvicorn main:app --reload
```

* `main`: O arquivo `main.py`.
* `app`: O objeto `app = FastAPI()` dentro do `main.py`.
* `--reload`: Reinicia o servidor automaticamente a cada alteração no código.

A API estará disponível em [http://127.0.0.1:8000](https://www.google.com/search?q=http://127.0.0.1:8000).

## 🧪 Testando o Endpoint de Webhook

Você pode testar o endpoint principal do bot usando `curl` ou um cliente de API (Postman, Insomnia).

**Bash**

```
curl -X 'POST' \
  'http://127.0.0.1:8000/api/v1/webhook' \
  -H 'Content-Type: application/json' \
  -d '{
    "user_id": "user123",
    "text": "Olá, mundo!"
  }'
```

**Resposta Esperada (Eco-Service):**

**JSON**

```
{
  "user_id": "user123",
  "response_text": "Você disse: 'Olá, mundo!'"
}
```

---
