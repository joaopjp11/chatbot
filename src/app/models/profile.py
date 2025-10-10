from sqlalchemy import Column, Integer, String, JSON, Text
from src.app.database.db import Base

class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), unique=True, index=True, nullable=False)
    idade = Column(Integer, nullable=True)
    formacao = Column(JSON, nullable=True) 
    experiencia = Column(JSON, nullable=True) 
    habilidades = Column(JSON, nullable=True) 
    objetivos = Column(Text, nullable=True)
    hobbies = Column(JSON, nullable=True)
