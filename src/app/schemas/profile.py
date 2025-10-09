from __future__ import annotations
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, model_validator


class Experience(BaseModel):
    empresa: str
    cargo: Optional[str] = None
    anos: Optional[int] = None


class ProfileBaseSchema(BaseModel):
    nome: str = Field(..., min_length=1)
    idade: Optional[int] = Field(None, ge=0, le=120)
    formacao: Optional[List[str]] = None
    experiencia: Optional[List[Experience]] = None
    habilidades: Optional[List[str]] = None
    objetivos: Optional[str] = None
    hobbies: Optional[List[str]] = None

    @model_validator(mode="before")
    def normalize_and_clean(cls, data: Dict[str, Any]):
        # Normalize single string values into lists for these fields
        for field in ["formacao", "habilidades", "hobbies"]:
            if field in data and isinstance(data[field], str):
                data[field] = [data[field]]

        # Trim whitespace and deduplicate habilidades
        if "habilidades" in data and data["habilidades"] is not None:
            cleaned: List[str] = []
            seen = set()
            for item in data["habilidades"]:
                if item is None:
                    continue
                s = str(item).strip()
                if not s:
                    continue
                if s.lower() in seen:
                    continue
                seen.add(s.lower())
                cleaned.append(s)
            data["habilidades"] = cleaned

        return data


class ProfileCreate(ProfileBaseSchema):
    pass


class ProfileUpdate(ProfileBaseSchema):
    pass


class ProfileOut(ProfileBaseSchema):
    # Output model can be identical to base but is separated for extensibility
    pass