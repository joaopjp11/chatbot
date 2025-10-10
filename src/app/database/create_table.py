from src.app.database.db import Base, engine
from src.app.models.profile import Profile

Base.metadata.create_all(bind=engine)
print("Tabelas criadas no PostgreSQL!")
