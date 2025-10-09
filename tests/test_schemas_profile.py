from src.app.schemas.profile import ProfileCreate


def test_habilidades_string_normalized_to_list():
    p = ProfileCreate(nome="Ana", habilidades="Python")
    assert isinstance(p.habilidades, list)
    assert p.habilidades == ["Python"]


def test_habilidades_deduplicated_and_trimmed():
    p = ProfileCreate(nome="Ana", habilidades=[" Python ", "python", ""])
    assert p.habilidades == ["Python"]
