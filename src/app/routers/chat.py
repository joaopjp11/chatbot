from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.app.services.chatbot import DigitalTwinChatbot
from src.app.utils.llm_interface import query_ollama
from src.app.utils.load_profiles import load_profiles

router = APIRouter(prefix="/chat", tags=["Chat"])

profiles = load_profiles()

class ChatRequest(BaseModel):
    pessoa: str
    pergunta: str

@router.post("/")
def chat_with_twin(req: ChatRequest):
    nome = req.pessoa.lower()
    if nome not in profiles:
        raise HTTPException(status_code=404, detail=f"Perfil '{req.pessoa}' não encontrado.")

    person = profiles[nome]
    chatbot = DigitalTwinChatbot(person)
    prompt = chatbot.build_prompt(req.pergunta)
    resposta = query_ollama(prompt)

    return {"pessoa": person.nome, "resposta": resposta}