from fastapi import APIRouter, HTTPException, status
from typing import List, Dict
from src.app.schemas.profile import ProfileCreate, ProfileUpdate, ProfileOut, ProfileBaseSchema
from src.app.utils.load_profiles import load_profiles
from fastapi import Depends
from src.app.utils.auth import verify_token


router = APIRouter(prefix="/profiles", tags=["Profiles"])

profiles: Dict[str, ProfileBaseSchema] = load_profiles()

@router.get("/", response_model=List[str])
def list_profiles():
    """Lista todos os perfis disponíveis."""
    return list(profiles.keys())

@router.get("/{nome}", response_model=ProfileOut)
def get_profile(nome: str):
    """Devolve um perfil específico."""
    key = nome.lower()
    if key not in profiles:
        raise HTTPException(status_code=404, detail=f"Perfil '{nome}' não encontrado.")
    return profiles[key]

@router.post("/", status_code=status.HTTP_201_CREATED, dependencies=[Depends(verify_token)])
def create_profile(profile: ProfileCreate):
    """Cria um novo perfil."""
    key = profile.nome.lower()
    if key in profiles:
        raise HTTPException(status_code=400, detail="Perfil já existe.")
    profiles[key] = ProfileBaseSchema(**profile.model_dump())
    return {"msg": f"Perfil '{profile.nome}' criado com sucesso."}

@router.put("/{nome}", dependencies=[Depends(verify_token)])
def update_profile(nome: str, profile: ProfileUpdate):
    """Atualiza um perfil existente."""
    key = nome.lower()
    if key not in profiles:
        raise HTTPException(status_code=404, detail="Perfil não encontrado.")
    updated_data = profile.dict(exclude_unset=True)
    for field, value in updated_data.items():
        setattr(profiles[key], field, value)
    return {"msg": f"Perfil '{nome}' atualizado com sucesso."}

@router.delete("/{nome}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(verify_token)])
def delete_profile(nome: str):
    """Apaga um perfil existente."""
    key = nome.lower()
    if key not in profiles:
        raise HTTPException(status_code=404, detail="Perfil não encontrado.")
    del profiles[key]
    return {"msg": f"Perfil '{nome}' apagado com sucesso."}
