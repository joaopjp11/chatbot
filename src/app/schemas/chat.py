from __future__ import annotations
from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    pessoa: str = Field(..., min_length=1)
    pergunta: str = Field(..., min_length=1)


class ChatResponse(BaseModel):
    pessoa: str
    resposta: str