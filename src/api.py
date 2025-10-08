from fastapi import FastAPI
from src.app.routers.chat import router as chat
from src.app.routers.profile import router as profile
from src.app.routers.web import web_router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="Digital Twin Chatbot API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat)
app.include_router(profile)
app.include_router(web_router)

@app.get("/")
def root():
    return {"message": "API do Digital Twin está ativa!"}
