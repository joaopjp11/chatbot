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
                white-space: pre-wrap;
                font-size: 16px;
                min-height: 50px;
            }
            /* Spinner de loading */
            .spinner {
                border: 4px solid #f3f3f3;
                border-top: 4px solid #4CAF50;
                border-radius: 50%;
                width: 24px;
                height: 24px;
                animation: spin 1s linear infinite;
                display: inline-block;
                vertical-align: middle;
                margin-left: 10px;
            }
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
            #loading {
                display: none;
            }
        </style>
    </head>
    <body>
        <h1>Digital Twin Chat</h1>
        <label for="pessoa">Pessoa:</label>
        <input type="text" id="pessoa" placeholder="Nome da pessoa" value=""/>

        <label for="pergunta">Pergunta:</label>
        <textarea id="pergunta" placeholder="Escreve a tua pergunta aqui..." rows="4"></textarea>

        <button id="enviarBtn" onclick="enviarPergunta()">Enviar</button>
        <span id="loading" class="spinner"></span>

        <h3>Resposta:</h3>
        <div id="resposta">A resposta aparecerá aqui...</div>

        <script>
            async function enviarPergunta() {
                const pessoa = document.getElementById('pessoa').value;
                const pergunta = document.getElementById('pergunta').value;
                const respostaDiv = document.getElementById('resposta');
                const loading = document.getElementById('loading');
                const enviarBtn = document.getElementById('enviarBtn');

                if (!pessoa || !pergunta) {
                    respostaDiv.textContent = "Por favor preenche todos os campos.";
                    return;
                }

                // Mostra o loading e desativa o botão
                loading.style.display = "inline-block";
                enviarBtn.disabled = true;
                respostaDiv.textContent = "";

                try {
                    const response = await fetch('/chat/', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ pessoa: pessoa, pergunta: pergunta })
                    });

                    const data = await response.json();

                    if (data.resposta) {
                        respostaDiv.textContent = data.resposta;
                    } else {
                        respostaDiv.textContent = JSON.stringify(data, null, 2);
                    }
                } catch (error) {
                    respostaDiv.textContent = "Erro ao enviar a pergunta.";
                } finally {
                    // Esconde o loading e reativa o botão
                    loading.style.display = "none";
                    enviarBtn.disabled = false;
                }
            }
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)
