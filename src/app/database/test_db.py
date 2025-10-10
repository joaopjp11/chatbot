from db import engine
from sqlalchemy import text

try:
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        print("Ligação bem-sucedida! Resultado:", result.scalar())
except Exception as e:
    print("Falha na ligação à base de dados:", e)