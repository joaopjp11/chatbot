# Digital Twin Chatbot

![Platform](https://img.shields.io/badge/platform-Windows-blue)
![Language](https://img.shields.io/badge/language-Python-lightgrey)

Chatbot em Python que simula um “digital twin” de uma pessoa e responde no terminal com base nos dados desse perfil.
Os perfis são ficheiros JSON na pasta profiles/. Ao iniciar, o programa pergunta com qual pessoa queres falar, carrega o JSON correspondente e usa um LLM local via Ollama para responder.


# Estrutura do Projeto
```text
.
├── src/
│ ├── person.py
│ ├── chatbot.py
│ ├── llm_interface.py
│ └── main.py
├── profiles/
│ ├── joao.json
│ ├── luis.json
│ ├── mafalda.json
│ └── ruben.json
├── poetry.lock
├── pyproject.toml
└── README.md
```

# Requisitos
- **Python** 3.10+
- **Poetry**
- **Ollama** (https://ollama.com)

## 🦙 Instalar o modelo **Llama 3.2 (3B)**

```bash
ollama pull llama3.2:3b


