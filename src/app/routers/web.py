from fastapi import APIRouter
from fastapi.responses import HTMLResponse

web_router = APIRouter(prefix="/web", tags=["web"])

@web_router.get("/", response_class=HTMLResponse)
def get_chat_page():
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Digital Twin Chat</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 40px;
                background-color: #f9f9f9;
            }
            h1 {
                color: #333;
            }
            input, textarea {
                width: 100%;
                padding: 10px;
                margin-bottom: 10px;
                border: 1px solid #ccc;
                border-radius: 5px;
                font-size: 16px;
            }
            button {
                padding: 10px 20px;
                font-size: 16px;
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
                cursor: pointer;
            }
            button:hover {
                background-color: #45a049;
            }
            #resposta {
                margin-top: 20px;
                padding: 15px;
                border-radius: 5px;
                background-color: #eef;
                border: 1px solid #99c;
                white-space: pre-wrap; /* mantém quebras de linha */
                font-size: 16px;
            }
        </style>
    </head>
    <body>
        <h1>Digital Twin Chat</h1>
        <label for="pessoa">Pessoa:</label>
        <input type="text" id="pessoa" placeholder="Nome da pessoa" value=""/>

        <label for="pergunta">Pergunta:</label>
        <textarea id="pergunta" placeholder="Escreve a tua pergunta aqui..." rows="4"></textarea>

        <button onclick="enviarPergunta()">Enviar</button>

        <h3>Resposta:</h3>
        <div id="resposta">A resposta aparecerá aqui...</div>

        <script>
            async function enviarPergunta() {
                const pessoa = document.getElementById('pessoa').value;
                const pergunta = document.getElementById('pergunta').value;

                const response = await fetch('/chat/', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ pessoa: pessoa, pergunta: pergunta })
                });

                const data = await response.json();

                // Transformar JSON em texto legível
                let text = '';
                if (data.resposta) {
                    text = data.resposta;
                } else {
                    text = JSON.stringify(data, null, 2);
                }

                document.getElementById('resposta').textContent = text;
            }
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

