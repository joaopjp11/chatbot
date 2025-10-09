import os
import shutil
import subprocess


def query_ollama(prompt: str, model: str = "llama3.2:3b") -> str:
    dev_mock = os.getenv("DEV_MOCK_LLM", "0").lower() in ("1", "true", "yes")

    ollama_path = shutil.which("ollama")
    if not ollama_path:
        msg = (
            "[ERRO] O comando 'ollama' não foi encontrado no PATH.\n"
            "Instale o cliente Ollama e assegure que 'ollama' está disponível no PATH,\n"
            "ou defina a variável de ambiente DEV_MOCK_LLM=1 para usar uma resposta mock durante o desenvolvimento."
        )
        if dev_mock:
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
        return (
            "[ERRO] Não foi possível executar 'ollama' — ficheiro não encontrado."
        )
    except Exception as e:
        return f"[ERRO] Falha ao consultar o modelo: {e}"