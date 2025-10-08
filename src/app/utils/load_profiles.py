import os
import json
from typing import Dict
from src.app.models.profile import ProfileBase 

DATA_DIR = "src/profiles"

def load_profiles() -> Dict[str, ProfileBase]:
    profiles: Dict[str, ProfileBase] = {}
    for filename in os.listdir(DATA_DIR):
        if filename.endswith(".json"):
            filepath = os.path.join(DATA_DIR, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
                profile = ProfileBase(**data) 
                profiles[profile.nome.lower()] = profile
    return profiles
