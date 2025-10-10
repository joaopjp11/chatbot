from fastapi import APIRouter, HTTPException, status, Depends
from typing import List, Dict
from src.app.schemas.profile import ProfileCreate, ProfileUpdate, ProfileOut, ProfileBaseSchema, Experience
from src.app.utils.auth import verify_token
from sqlalchemy.orm import Session
from src.app.database.db import SessionLocal
from src.app.models.profile import Profile
from src.app.database.load_bd_profiles import (
    get_profile_by_name, 
    get_all_profiles, 
    create_profile as db_create_profile,
    update_profile as db_update_profile,
    delete_profile as db_delete_profile
)

router = APIRouter(prefix="/profiles", tags=["Profiles"])

# Dependency para obter sessão DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[str])
def list_profiles(db: Session = Depends(get_db)):
    profiles = get_all_profiles(db)
    return [p.nome for p in profiles]

@router.get("/{nome}", response_model=ProfileOut)
def get_profile(nome: str, db: Session = Depends(get_db)):
    profile = get_profile_by_name(db, nome)
    if not profile:
        raise HTTPException(status_code=404, detail=f"Perfil '{nome}' não encontrado.")
    
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
    
    return ProfileOut(**profile_data)

@router.post("/", status_code=status.HTTP_201_CREATED, dependencies=[Depends(verify_token)])
def create_profile(profile: ProfileCreate, db: Session = Depends(get_db)):
    """Cria um novo perfil."""
    # Check if profile already exists
    existing_profile = get_profile_by_name(db, profile.nome)
    if existing_profile:
        raise HTTPException(status_code=400, detail="Perfil já existe.")
    
    # Create new profile in database
    db_create_profile(db, profile)
    return {"msg": f"Perfil '{profile.nome}' criado com sucesso."}

@router.put("/{nome}", dependencies=[Depends(verify_token)])
def update_profile(nome: str, profile: ProfileUpdate, db: Session = Depends(get_db)):
    """Atualiza um perfil existente."""
    updated_profile = db_update_profile(db, nome, profile)
    if not updated_profile:
        raise HTTPException(status_code=404, detail="Perfil não encontrado.")
    return {"msg": f"Perfil '{nome}' atualizado com sucesso."}

@router.delete("/{nome}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(verify_token)])
def delete_profile(nome: str, db: Session = Depends(get_db)):
    """Apaga um perfil existente."""
    deleted = db_delete_profile(db, nome)
    if not deleted:
        raise HTTPException(status_code=404, detail="Perfil não encontrado.")
    return {"msg": f"Perfil '{nome}' apagado com sucesso."}
