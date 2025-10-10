from sqlalchemy.orm import Session
from src.app.models.profile import Profile
from src.app.schemas.profile import ProfileCreate, ProfileUpdate

def get_profile_by_name(db: Session, nome: str) -> Profile | None:
    return db.query(Profile).filter(Profile.nome.ilike(nome)).first()

def get_all_profiles(db: Session) -> list[Profile]:
    return db.query(Profile).all()

def create_profile(db: Session, profile_data: ProfileCreate) -> Profile:
    """Create a new profile in the database"""
    # Convert Experience objects to dictionaries for JSON storage
    experiencia_dicts = []
    if profile_data.experiencia:
        for exp in profile_data.experiencia:
            if hasattr(exp, 'model_dump'):
                experiencia_dicts.append(exp.model_dump())
            else:
                experiencia_dicts.append(exp)
    
    db_profile = Profile(
        nome=profile_data.nome,
        idade=profile_data.idade,
        formacao=profile_data.formacao,
        experiencia=experiencia_dicts,
        habilidades=profile_data.habilidades,
        objetivos=profile_data.objetivos,
        hobbies=profile_data.hobbies
    )
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile

def update_profile(db: Session, nome: str, profile_data: ProfileUpdate) -> Profile | None:
    """Update an existing profile in the database"""
    db_profile = get_profile_by_name(db, nome)
    if not db_profile:
        return None
    
    # Convert Experience objects to dictionaries for JSON storage
    experiencia_dicts = []
    if profile_data.experiencia:
        for exp in profile_data.experiencia:
            if hasattr(exp, 'model_dump'):
                experiencia_dicts.append(exp.model_dump())
            else:
                experiencia_dicts.append(exp)
    
    # Update only the fields that are provided
    update_data = profile_data.model_dump(exclude_unset=True)
    if 'experiencia' in update_data and update_data['experiencia'] is not None:
        update_data['experiencia'] = experiencia_dicts
    
    for field, value in update_data.items():
        setattr(db_profile, field, value)
    
    db.commit()
    db.refresh(db_profile)
    return db_profile

def delete_profile(db: Session, nome: str) -> bool:
    """Delete a profile from the database"""
    db_profile = get_profile_by_name(db, nome)
    if not db_profile:
        return False
    
    db.delete(db_profile)
    db.commit()
    return True