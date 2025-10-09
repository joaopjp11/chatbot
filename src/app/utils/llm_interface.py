import os
import shutil
import subprocess


def query_ollama(prompt: str, model: str = "llama3.2:3b") -> str:
    """
    Envia um prompt para o modelo Ollama e devolve a resposta.

    If the `ollama` binary is not available in PATH this function will either
    return a helpful error message or (if the environment variable
    `DEV_MOCK_LLM` is set) return a small canned response so the app can be
    developed/tested without installing Ollama.
    """
    # Optional developer mock to avoid requiring Ollama during local dev/tests
    dev_mock = os.getenv("DEV_MOCK_LLM", "0").lower() in ("1", "true", "yes")

    ollama_path = shutil.which("ollama")
    if not ollama_path:
        msg = (
            "[ERRO] O comando 'ollama' não foi encontrado no PATH.\n"
            "Instale o cliente Ollama e assegure que 'ollama' está disponível no PATH,\n"
            "ou defina a variável de ambiente DEV_MOCK_LLM=1 para usar uma resposta mock durante o desenvolvimento."
        )
        if dev_mock:
            # Return a predictable mocked response so front-end/dev flows can proceed
            return f"[MOCK] Resposta simulada para o prompt: {prompt[:200]}"
        return msg

    try:
        result = subprocess.run(
            [ollama_path, "run", model],
            input=prompt.encode("utf-8"),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        if result.returncode != 0:
            stderr = result.stderr.decode("utf-8", errors="ignore").strip()
            return f"[ERRO] Ollama retornou código {result.returncode}: {stderr}"

        output = result.stdout.decode("utf-8", errors="ignore").strip()
        return output
    except FileNotFoundError:
        # Shouldn't happen because we used shutil.which, but be defensive
        return (
            "[ERRO] Não foi possível executar 'ollama' — ficheiro não encontrado."
        )
    except Exception as e:
        return f"[ERRO] Falha ao consultar o modelo: {e}"