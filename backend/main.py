import os
import datetime
import joblib
import firebase_admin
from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient
from firebase_admin import credentials, auth
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

# 1. CARREGAR CONFIGURAÇÕES DO .ENV
load_dotenv()

# 2. CONFIGURAÇÃO FIREBASE (USA O .ENV)
firebase_creds = {
    "type": "service_account",
    "project_id": os.getenv("FIREBASE_PROJECT_ID"),
    "private_key": os.getenv("FIREBASE_PRIVATE_KEY").replace('\\n', '\n'),
    "client_email": os.getenv("FIREBASE_CLIENT_EMAIL"),
    "token_uri": "https://oauth2.googleapis.com/token",
}

# Inicializa o Firebase apenas se não tiver sido inicializado
if not firebase_admin._apps:
    cred = credentials.Certificate(firebase_creds)
    firebase_admin.initialize_app(cred)

app = FastAPI()

# 3. MIDDLEWARE CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 4. CONFIGURAÇÃO DO BANCO DE DADOS (USA O .ENV)
# No seu .env, coloque MONGODB_URL=sua_url_aqui
MONGO_URL = os.getenv("MONGODB_URL") 
client = AsyncIOMotorClient(MONGO_URL)
db = client.chatbot_db
collection = db.historico_mensagens

# 5. CARREGAR IA
modelo = joblib.load('models/modelo_ia.pkl')
vectorizer = joblib.load('models/vectorizer.pkl')

class MensagemUsuario(BaseModel):
    texto: str

@app.post("/chat")
async def responder_chat(mensagem: MensagemUsuario, authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Token ausente")
    
    try:
        # Extrai o token removendo a palavra 'Bearer '
        token = authorization.split("Bearer ")[1]
        # VALIDA o token com o Firebase
        decoded_token = auth.verify_id_token(token)
        usuario_id = decoded_token['uid']
    except Exception:
        raise HTTPException(status_code=401, detail="Token inválido")

    # 6. IA PROCESSA A MENSAGEM
    texto_vet = vectorizer.transform([mensagem.texto])
    categoria = modelo.predict(texto_vet)[0]
    
    # LOG para você ver no painel do Render o que a IA detectou
    print(f"Mensagem: {mensagem.texto} | Categoria Detectada: {categoria}")

    respostas = {
        'Pagamento': 'Boleto disponível no app.',
        'Suporte': 'Tente reiniciar o app ou limpar o cache.',
        'Reclamação': 'Lamentamos o ocorrido. Registramos sua queixa.',
        'Consulta': 'Seu saldo atualizado está na tela de início.'
    }
    
    # Procura a resposta (usando .strip() para evitar espaços invisíveis)
    # Se a IA prever 'Pagamento ' ou 'pagamento', o código abaixo trata melhor
    reply = respostas.get(categoria, "Não entendi bem, mas vou encaminhar para um atendente.")

    
    # 7. SALVAR NO MONGODB
    log_interacao = {
        "usuario_msg": mensagem.texto,
        "ia_intent": categoria,
        "ia_reply": reply,
        "data": datetime.datetime.utcnow()
    }
    await collection.insert_one(log_interacao)

    return {"intent": categoria, "reply": reply}

@app.get("/")
def home():
    return {"status": "Servidor e IA Online"}