import subprocess

def query_ollama(prompt: str, model: str = "llama3.2:3b") -> str:
    """
    Envia um prompt para o modelo Ollama e devolve a resposta.
    """
    try:
        result = subprocess.run(
            ["ollama", "run", model],
            input=prompt.encode("utf-8"),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        output = result.stdout.decode("utf-8").strip()
        return output
    except Exception as e:
        return f"[ERRO] Falha ao consultar o modelo: {e}"