from src.app.utils.llm_interface import query_ollama
from src.app.models.profile import ProfileBase

class DigitalTwinChatbot:
    def __init__(self, profile: ProfileBase):
        self.profile = profile

    def build_prompt(self, user_input: str) -> str:
        """
        Cria o contexto que será enviado ao modelo com base nos dados do perfil.
        """
        context_parts = [
            f"Nome: {self.profile.nome}",
            f"Idade: {self.profile.idade}" if self.profile.idade else "",
            f"Formação: {self.profile.formacao}" if self.profile.formacao else "",
            f"Experiência: {self.profile.experiencia}" if self.profile.experiencia else "",
            f"Habilidades: {', '.join(self.profile.habilidades)}" if self.profile.habilidades else "",
            f"Objetivos: {self.profile.objetivos}" if self.profile.objetivos else "",
            f"Hobbies: {', '.join(self.profile.hobbies)}" if self.profile.hobbies else ""
        ]
        context = "\n".join([c for c in context_parts if c])

        prompt = (
            f"Tu és {self.profile.nome}, e vais responder às perguntas como se fosses essa pessoa.\n"
            f"Abaixo estão informações sobre ti:\n{context}\n\n"
            f"Pergunta: {user_input}\n"
            f"Resposta:"
        )
        return prompt
