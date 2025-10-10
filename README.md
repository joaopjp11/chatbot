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
│ │ ├── models/
│ │ │ └── profile.py # Modelos Pydantic para validação dos perfis
│ │ │
│ │ ├── routers/ # Rotas principais da API
│ │ │ ├── chat.py # Endpoint /chat — interação com os gêmeos digitais
│ │ │ ├── profile.py # Endpoint /profiles — CRUD de perfis
│ │ │ └── web.py # Endpoint /web — interface HTML simples
│ │ │
│ │ └── services/
| | | └── chatbot.py # Lógica do chatbot e geração de prompts personalizados
│ │ │
│ │ └── utils/
| | | ├── llm_interface.py # Interface com o modelo Ollama (execução do LLM)
│ │ | └── load_profiles.py # Carregamento automático de perfis JSON
├── poetry.lock
├── pyproject.toml
└── README.md

```

# Requisitos
- **Python** 3.10+
- **Poetry**
- **PostgreSQL** (servidor local ou remoto)

## Instalar dependências com o Poetry
```bash
poetry install
```

## 🗄️ Configurar Base de Dados PostgreSQL

**Antes de executar o projeto, é necessário configurar a base de dados:**

1. **Instalar PostgreSQL** (se ainda não tiver)
2. **Configurar senha do admin** no ficheiro `smart_db_setup.py` (linha 28)
3. **Executar o setup da base de dados:**

```bash
python smart_db_setup.py
```

Este script irá automaticamente:
- ✅ Criar utilizador PostgreSQL (`chatbot_user`)
- ✅ Criar base de dados (`digital_twin`) 
- ✅ Criar tabelas necessárias
- ✅ Carregar perfis dos ficheiros JSON

**Nota:** Pode executar este comando várias vezes com segurança. Se a base de dados já existir, apenas verificará o estado.

## 🦙 Instalar o modelo **Llama 3.2 (3B)**

```bash
ollama pull llama3.2:3b
```

## Correr Projeto

**Após configurar a base de dados:**

```bash
poetry run uvicorn src.api:app --reload
```
## Aceder ao Chat na Web
http://localhost:8000/web

