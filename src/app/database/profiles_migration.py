import os, json
from src.app.database.db import SessionLocal
from src.app.models.profile import Profile

db = SessionLocal()
DATA_DIR = "src/profiles"

for filename in os.listdir(DATA_DIR):
    if filename.endswith(".json"):
        data = json.load(open(os.path.join(DATA_DIR, filename), encoding="utf-8"))
        db.add(Profile(**data))

db.commit()
db.close()
print("Perfis migrados para PostgreSQL!")
