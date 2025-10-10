import os, json
from src.app.database.db import SessionLocal
from src.app.models.profile import Profile

db = SessionLocal()
DATA_DIR = "src/profiles"

for filename in os.listdir(DATA_DIR):
    if filename.endswith(".json"):
        data_path = os.path.join(DATA_DIR, filename)
        with open(data_path, encoding="utf-8") as f:
            data = json.load(f)
        
        existing = db.query(Profile).filter(Profile.nome.ilike(data["nome"])).first()
        if existing:
            print(f"Perfil '{data['nome']}' já existe na base de dados. Ignorando...")
            continue

        db.add(Profile(**data))
        print(f"Perfil '{data['nome']}' adicionado à base de dados.")

db.commit()
db.close()
print("Migração concluída!")
