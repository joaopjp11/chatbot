from typing import List, Dict, Any
from pydantic import BaseModel, model_validator

class ProfileBase(BaseModel):
    nome: str
    idade: int | None = None
    formacao: List[str] | None = None
    experiencia: List[Dict[str, Any]] | None = None
    habilidades: List[str] | None = None
    objetivos: str | None = None
    hobbies: List[str] | None = None

    @model_validator(mode="before")
    def normalize_lists(cls, data):
        for field in ["formacao", "habilidades", "hobbies"]:
            if field in data and isinstance(data[field], str):
                data[field] = [data[field]]
        return data

class ProfileCreate(ProfileBase):
    pass

class ProfileUpdate(ProfileBase):
    pass
