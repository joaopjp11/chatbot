# Digital Twin Chatbot

![Platform](https://img.shields.io/badge/platform-Windows-blue)
![Language](https://img.shields.io/badge/language-Python-lightgrey)

Chatbot em Python que simula um “digital twin” de uma pessoa com base nos dados do perfil dessa pessoa.


# Estrutura do Projeto
```text
.
├── api.py # Ponto de entrada da aplicação FastAPI
│
├── src/
│ ├── profiles/ # Perfis JSON dos digitais twins
│ │ ├── joao.json
│ │ ├── luis.json
│ │ ├── mafalda.json
│ │ └── ruben.json
│ │
│ ├── app/
│ │ ├── database/
│ │ │ ├── db.py # Gere a ligação à base de dados
│ │ │ └── load_db_profiles.py # Funções para Visualizar, Criar, Atualizar e Apagar perfis na base de dados
│ │ │
│ │ ├── models/
│ │ │ └── profile.py # Modelos SQLAlchemy para a tabela "profiles"
│ │ │
│ │ ├── routers/ # Rotas principais da API
│ │ │ ├── chat.py # Endpoint /chat — interação com os gêmeos digitais
│ │ │ ├── profile.py # Endpoint /profiles — CRUD de perfis
│ │ │ └── web.py # Endpoint /web — interface HTML simples
│ │ │
│ │ └── schemas/
│ │ │ ├── chat.py Modelos Pydantic para validação do chatbot
│ │ │ ├── profile.py Modelos Pydantic para validação dos perfis
| | |
│ │ └── services/
| | | └── chatbot.py # Lógica do chatbot e geração de prompts personalizados
│ │ │
│ │ └── utils/
| | | ├── auth.py # Autenticação
| | | ├── llm_interface.py # Interface com o modelo Ollama (execução do LLM)
│ │ | └── load_profiles.py # Carregamento automático de perfis JSON
│ 
├── smart_db_setup.py # Setup inicial da Base de dados e respetivas tabelas e dados
├── poetry.lock
├── pyproject.toml
└── README.md

```

# Requisitos
- **Python** 3.10+
- **Poetry**
- **PostgreSQL**

## Instalar dependências com o Poetry
```bash
poetry install
```
- **Ollama** (https://ollama.com)
## 🦙 Instalar o modelo **Llama 3.2 (3B)**

```bash
ollama pull llama3.2:3b
```
## Setup Base de Dados
### No smart_db_setup.py modificar line: 27/28 para corresponder à realidade do utilizador
```python
ADMIN_USER = "pgAdmin username"
ADMIN_PASSWORD = os.getenv("POSTGRES_PASSWORD", "pgAdmin password")
```
```bash
poetry run python smart_db_setup.py
```
## Correr Projeto
```bash
poetry run uvicorn src.api:app --reload
```
## Aceder ao Chat na Web
http://localhost:8000/web

## Aceder ao /docs
http://localhost:8000/docs
