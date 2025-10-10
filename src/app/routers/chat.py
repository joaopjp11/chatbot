from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from src.app.services.chatbot import DigitalTwinChatbot
from src.app.utils.llm_interface import query_ollama
from src.app.schemas.chat import ChatRequest, ChatResponse
from src.app.schemas.profile import ProfileBaseSchema, Experience
from src.app.database.db import SessionLocal
from src.app.database.load_bd_profiles import get_profile_by_name

router = APIRouter(prefix="/chat", tags=["Chat"])

# Dependency para obter sessão DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=ChatResponse)
def chat_with_twin(req: ChatRequest, db: Session = Depends(get_db)):
    # Get profile from database
    profile = get_profile_by_name(db, req.pessoa)
    if not profile:
        raise HTTPException(status_code=404, detail=f"Perfil '{req.pessoa}' não encontrado.")

    # Convert SQLAlchemy model to Pydantic schema
    experiencia_list = []
    if profile.experiencia:
        for exp in profile.experiencia:
            if isinstance(exp, dict):
                experiencia_list.append(Experience(**exp))
            else:
                experiencia_list.append(exp)
    
    profile_data = {
        "nome": profile.nome,
        "idade": profile.idade,
        "formacao": profile.formacao or [],
        "experiencia": experiencia_list,
        "habilidades": profile.habilidades or [],
        "objetivos": profile.objetivos,
        "hobbies": profile.hobbies or []
    }
    
    person = ProfileBaseSchema(**profile_data)
    chatbot = DigitalTwinChatbot(person)
    prompt = chatbot.build_prompt(req.pergunta)
    resposta = query_ollama(prompt)

    return ChatResponse(pessoa=person.nome, resposta=resposta)